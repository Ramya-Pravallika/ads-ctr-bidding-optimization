from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/usr/local/airflow/src')
from utils.synthetic_data import generate_synthetic_ctr_data
from data_processing.spark_feature_engineering import aggregate_features
from model.ctr_dnn_fm_ffm import build_ctr_model
import mlflow

def pipeline():
    # 1. Data generation
    df_raw = generate_synthetic_ctr_data()
    # 2. Spark feature agg (assuming local Spark context)
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.master("local[*]").appName("CTR-Pipeline").getOrCreate()
    df_features = aggregate_features(spark, df_raw)
    # 3. Model training
    n_ads = df_features['ad_id'].nunique()
    n_users = df_features['user_id'].nunique()
    n_campaigns = df_features['campaign_id'].nunique()
    n_cats = df_features['ad_category'].nunique()
    n_devices = df_features['device'].nunique()
    model = build_ctr_model(n_ads, n_users, n_campaigns, n_cats, n_devices)
    X = [
        df_features['ad_id'].values,
        df_features['user_id'].values,
        df_features['campaign_id'].values,
        df_features['ad_category'].astype('category').cat.codes.values,
        df_features['device'].astype('category').cat.codes.values
    ]
    y = (df_features['ctr'] > 0.1).astype(int).values  # binary: high ctr or not
    mlflow.set_experiment('ctr_dnn')
    with mlflow.start_run():
        history = model.fit(X, y, epochs=5, batch_size=256)
        mlflow.log_metric('final_auc', history.history['auc'][-1])
        mlflow.keras.log_model(model, 'model')
    spark.stop()

dag = DAG(
    'ctr_ads_pipeline',
    default_args={'owner': 'airflow'},
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
)

pipeline_task = PythonOperator(
    task_id='run_ctr_pipeline',
    python_callable=pipeline,
    dag=dag
)
