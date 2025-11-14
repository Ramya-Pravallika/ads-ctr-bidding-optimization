import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Flatten, Concatenate, Dropout
from tensorflow.keras.models import Model

def build_ctr_model(num_ads, num_users, num_campaigns, num_ad_categories, num_devices):
    ad_id_in = Input(shape=(1,), name='ad_id')
    user_id_in = Input(shape=(1,), name='user_id')
    campaign_id_in = Input(shape=(1,), name='campaign_id')
    ad_cat_in = Input(shape=(1,), name='ad_category')
    device_in = Input(shape=(1,), name='device')
    
    embed_ad = Embedding(num_ads+1, 8)(ad_id_in)
    embed_user = Embedding(num_users+1, 8)(user_id_in)
    embed_campaign = Embedding(num_campaigns+1, 3)(campaign_id_in)
    embed_cat = Embedding(num_ad_categories+1, 3)(ad_cat_in)
    embed_device = Embedding(num_devices+1, 2)(device_in)

    features = Concatenate()([
        Flatten()(embed_ad),
        Flatten()(embed_user),
        Flatten()(embed_campaign),
        Flatten()(embed_cat),
        Flatten()(embed_device)
    ])
    x = Dense(64, activation='relu')(features)
    x = Dropout(0.3)(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.2)(x)
    out = Dense(1, activation='sigmoid')(x)
    model = Model([ad_id_in, user_id_in, campaign_id_in, ad_cat_in, device_in], out)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['AUC'])
    return model
