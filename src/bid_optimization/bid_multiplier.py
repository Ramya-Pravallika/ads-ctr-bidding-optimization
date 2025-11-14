import numpy as np

def optimal_bid_multiplier(predicted_ctr, base_bid, value_per_click):
    ev = predicted_ctr * value_per_click - base_bid
    multiplier = np.clip(ev / base_bid, 0.5, 3.0)
    return multiplier
