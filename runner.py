import pandas as pd
import numpy as np
import aggregator as agg
import clusterer as clt
import pickle


print("aggregating data...")
data = pd.read_csv("dataset_gps.csv", sep=";").drop(columns="Unnamed: 0")
# data = pd.read_csv("hackprague_txs_reduced_gps.csv", sep=";")
# clients = pd.read_csv("clients.csv")["client_id"]
clients = data["client_id"].unique()
print(len(clients))
print("aggregating data...")
for i in range(45000, len(clients)+1, 5000):
    tot = []
    print(i)
    for client_id in clients[i:i+5000]:
        tot.append(agg.aggregate_data(data[data["client_id"] == client_id]))
    pd.concat(tot).to_csv(f"clients_agg_{i+5000}.csv",index=None)

print("loading data...")
complete = []
for i in range(0, len(clients)+1, 5000):
    complete.append(pd.read_csv(f"clients_agg_{i+5000}.csv", index_col="client_id"))
agg_data = pd.concat(complete)


count_cols = []
sum_cols = []
for col in agg_data.columns:
    if col.startswith("count "):
        count_cols.append(col)
    if col.startswith("sum "):
        sum_cols.append(col)

print("creating clusters...")

no_sum_clusters = []
no_count_clusters = []
for i in range(6, 30, 2):
    no_sum_clusters.append(clt.cluster_clients(no_sum_data, i).labels_)
    no_count_clusters.append(clt.cluster_clients(no_count_data, i).labels_)
    
    # now check the differnet clusters and choose the best...

