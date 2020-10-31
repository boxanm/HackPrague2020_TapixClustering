import pandas as pd
import numpy as np

def aggregate_data(client_data):
    st_spending = client_data.groupby(client_data["shop_type"]).amount.agg(["sum", "count", "mean"]) 

    st_count = st_spending["count"]
    st_count.index = "count " + st_count.index

    st_mean = st_spending["mean"]
    st_mean.index = "mean " + st_mean.index

    st_sum = st_spending["sum"]
    st_sum.index = "sum " + st_sum.index


    cat_spending = client_data.groupby(client_data["merchant_category"]).amount.agg(["sum", "count", "mean"]) 

    c_count = cat_spending["count"]
    c_count.index = "count " + c_count.index

    c_mean = cat_spending["mean"]
    c_mean.index = "mean " + c_mean.index

    c_sum = cat_spending["sum"]
    c_sum.index = "sum " + c_sum.index

    client_data["shop_tags"] = client_data["shop_tags"].str.replace("{|}", "").str.split(",")
    tag_spending = client_data.explode("shop_tags").groupby("shop_tags").amount.agg(["sum", "count", "mean"]) 

    t_count = tag_spending["count"]
    t_count.index = "count " + t_count.index

    t_mean = tag_spending["mean"]
    t_mean.index = "mean " + t_mean.index

    t_sum = tag_spending["sum"]
    t_sum.index = "sum " + t_sum.index

    agg_data = {
        "client_id": client_data.iloc[0]["client_id"],
        "client_gender": client_data.iloc[0]["client_gender"],
        "client_year_of_birth": client_data.iloc[0]["client_year_of_birth"],
        "spending": client_data["amount"].sum(),
        "count": client_data["client_id"].count(),
        **c_count,
        **c_mean,
        **c_sum,
        **t_count,
        **t_mean,
        **t_sum,
        **st_count,
        **st_mean,
        **st_sum,
    }
    
    return pd.DataFrame([agg_data])