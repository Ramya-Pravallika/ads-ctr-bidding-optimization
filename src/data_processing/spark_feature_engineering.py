from pyspark.sql import SparkSession
import pandas as pd

def aggregate_features(spark: SparkSession, df: pd.DataFrame):
    sdf = spark.createDataFrame(df)
    sdf.createOrReplaceTempView('ads')
    agg_query = """
    SELECT
        ad_id,
        user_id,
        campaign_id,
        ad_category,
        time_of_day,
        device,
        COUNT(*) AS impressions,
        SUM(clicked) AS clicks,
        AVG(clicked) AS ctr
    FROM ads
    GROUP BY ad_id, user_id, campaign_id, ad_category, time_of_day, device
    """
    return spark.sql(agg_query).toPandas()
