import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from matplotlib import pyplot as plt

weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
numOfClusters = 4

def categories_to_columns(transaction_data, categories):
    for cat in categories:
        if (transaction_data['merchant_category'] == cat):
            return cat


def weekdays_to_columns(transaction_data):
    return weekDays[pd.to_datetime(transaction_data['tx_date']).dayofweek]


def normalize(user):
    user[['amount', 'Longitude', 'Latitude']] = preprocessing.scale(user[['amount', 'Longitude', 'Latitude']])
    return user


def reshape_user(user_data, categories):
    user_reshaped = user_data.copy()
    for cat in categories:
        user_reshaped.insert(len(user_data.columns), cat, 0)

    for day in weekDays:
        user_reshaped.insert(len(user_data.columns), day, 0)

    for index, row in user_data.iterrows():
        cat = categories_to_columns(row, categories)
        user_reshaped.loc[index, cat] = 1
        day = weekdays_to_columns(row)
        user_reshaped.loc[index, day] = 1
    user_reshaped.drop('merchant_category', axis=1, inplace=True)
    user_reshaped.drop('tx_date', axis=1, inplace=True)
    return user_reshaped


def get_user(data, cats, user_id):
    user = data[data['client_id'] == user_id].copy()
    return preprocess_user(user, cats)


def preprocess_user(user, cats):
    # user.sort_values(by=["tx_date", 'amount'], ascending=[True, False], inplace=True)
    user.drop(['client_year_of_birth', 'client_id', 'client_gender', 'shop_type', 'shop_tags',
               'merchant_category_id', 'merchant_uid', 'shop_uid', 'region', 'country',
               'transaction_id'], axis=1, inplace=True)
    user = reshape_user(user, cats)

    return user

def preprocess_transaction(transaction, cats):
    transaction.drop(['client_year_of_birth', 'client_id', 'client_gender', 'shop_type', 'shop_tags',
               'merchant_category_id', 'merchant_uid', 'shop_uid', 'region', 'country',
               'transaction_id'], inplace=True)
    transaction = reshape_user(transaction, cats)

    return transaction

def get_distance_from_means(means, point):
    values = []
    for mean in means:
        values.append(np.linalg.norm(mean - point))
    return [np.linalg.norm(means - point), np.array(values).T]


def cluster_user_transaction(user):
    kmeans = KMeans(n_clusters=numOfClusters).fit(user)
    centroids = kmeans.cluster_centers_
    # print(kmeans.labels_)

    # Nice Pythonic way to get the indices of the points for each corresponding cluster
    mydict = {i: np.where(kmeans.labels_ == i)[0] for i in range(kmeans.n_clusters)}

    # Transform this dictionary into list (if you need a list as result)
    dictlist = []
    for key, value in mydict.items():
        temp = [key, value]
        dictlist.append(temp)
    return centroids, dictlist



def check_transaction(data, categories, transaction):
    user_id = transaction['client_id'].values[0]

    user = get_user(data, categories, user_id)
    transaction2 = preprocess_user(transaction.copy(), cats)

    # normalize
    user = pd.concat([user, transaction2])
    user = normalize(user)
    transaction2 = pd.DataFrame(user.iloc[len(user) -1]).copy().transpose()
    user = user[:-1]
    means, clusters = cluster_user_transaction(user)

    distance_total = np.zeros([len(user)])
    distances = np.zeros([len(user),numOfClusters])
    for i in range(len(user)):
        distance_total[i], distances[i][:] = get_distance_from_means(means, user.iloc[i].values)

    trans_distance_total, trans_distances = get_distance_from_means(means, transaction2.values)

    cluster_idx = np.where(abs(trans_distance_total - distance_total) == np.amin(abs(trans_distance_total - distance_total)))[0]
    this_user = data[data['client_id'] == user_id]

    indexes = []
    for v in clusters:
        indexes.append(this_user.transaction_id.values[v[1]])

    this_user_cluster = this_user[this_user.index.isin(indexes[cluster_idx[0]])]
    # print('Contains shop id: ', transaction['shop_uid'].values[0] in this_user_cluster['shop_uid'].values)

    return not transaction['shop_uid'].values[0] in this_user_cluster['shop_uid'].values



    # plot distances to see if clusters were generated meaningfully
    # f1 = plt.plot(distance_total)
    # f2 = plt.figure()
    #
    # indexes = []
    # for v in clusters:
    #     indexes.append(user.index.values[v[1]])
    #
    # for i in range(numOfClusters):
    #     cluster_indeces = indexes[i]
    #     this_user = data[data['client_id'] == user_id]
    #     print(this_user[this_user.index.isin(cluster_indeces)])
    #
    #     plt.subplot(2,2,i+1)
    #     plt.scatter(clusters[i][1], distances[clusters[i][1], i])
    #     plt.plot(distances[:, i])
    #
    # plt.show()



if __name__ == '__main__':
    data = pd.read_csv('hackprague_txs_reduced_gps.csv', sep=";")
    data.dropna(inplace=True)
    data.drop(data[data['country'] != 'CZ'].index, inplace=True)
    data.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
    cats = data["merchant_category"].unique()

    idx = 25
    transaction = pd.DataFrame(data.iloc[idx]).copy().transpose()
    transaction['shop_uid'] = ['dsafasfas']

    print("Should we recommend this transaction? ", check_transaction(data, cats, transaction))