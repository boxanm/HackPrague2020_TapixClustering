import pandas as pd
import numpy as np
import requests
import urllib.parse


def main():
    data = pd.read_csv('hackprague_txs.csv', sep=";")
    # data = pd.read_csv('hackprague_txs2.csv', sep=",")
    data.dropna(inplace=True)
    data.drop(data[data['country'] != 'CZ'].index, inplace=True)
    data.sort_values(by=["region", 'shop_uid'], ascending=[True, True], inplace=True)
    data.insert(len(data.columns), 'Latitude', np.nan)
    data.insert(len(data.columns), 'Longitude', np.nan)
    n = np.linspace(1, len(data), len(data))
    data.reset_index(inplace=True)
    regions = data['region'].unique()
    regions_shops = {}
    print("Celkem unikátních obchodů: %d" %(len(data['shop_uid'].unique())))
    idx_prev = 0
    for region in regions:
        datar = data[data['region'] == region]
        regions_shops[region] = datar['shop_uid'].unique()
        print('------------------------------------Getting coordinates for region %s shops: %d' %(region, len(regions_shops[region])))
        [x, y] = get_coordinates(region, regions_shops[region])
        if len(x) > 0 and len(y) > 0:
            for shop_idx in range(len(regions_shops[region])):
                id = regions_shops[region][shop_idx]
                num_of_shops = len(data[data['shop_uid'] == id]['shop_uid'])
                print('number of shops with id %s : %d\tidx_prev %d' %(id, num_of_shops, idx_prev))
                data.loc[idx_prev:idx_prev+num_of_shops - 1, ['Latitude', 'Longitude']] = [x[shop_idx], y[shop_idx]]

                idx_prev = idx_prev + num_of_shops

    data.to_csv('dataset_gps.csv', sep=";")


def get_coordinates(region_name, shop_ids):
    try:
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(
            region_name) + '?format=json'

        response = requests.get(url).json()
        mean = [float(response[0]["lat"]), float(response[0]["lon"])]
    except:
        return [[], []]

    cov = [[0.01, 0], [0, 0.01]]

    x, y = np.random.multivariate_normal(mean, cov, len(shop_ids)).T

    # plt.plot(x, y, 'x')
    # plt.scatter(mean[0], mean[1], s=80)
    # plt.title(region_name)
    # plt.axis('equal')
    # plt.show()

    return [x, y]


if __name__ == '__main__':
    main()
