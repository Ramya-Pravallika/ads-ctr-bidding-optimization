import pandas as pd
import numpy as np

def generate_synthetic_ctr_data(n_rows=100000):
    np.random.seed(42)
    df = pd.DataFrame({
        'ad_id': np.random.randint(1, 1000, size=n_rows),
        'user_id': np.random.randint(1, 50000, size=n_rows),
        'session_id': np.random.randint(1, 20000, size=n_rows),
        'campaign_id': np.random.randint(1, 100, size=n_rows),
        'ad_category': np.random.choice(['sports', 'tech', 'fashion', 'food', 'travel'], size=n_rows),
        'time_of_day': np.random.choice(['morning', 'afternoon', 'evening', 'night'], size=n_rows),
        'device': np.random.choice(['mobile', 'desktop', 'tablet'], size=n_rows),
        'clicked': np.random.binomial(1, 0.11, size=n_rows)
    })
    return df
