from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans


def cluster_clients(cli_data, n_clusters):
    cli_data.replace(np.nan, 0, inplace=True)
    cli_data.replace('Male', 1, inplace=True)
    cli_data.replace('Female', 0, inplace=True)

    x = cli_data.values 
    scaled = preprocessing.scale(x)
    return KMeans(n_clusters=n_clusters).fit(scaled)
