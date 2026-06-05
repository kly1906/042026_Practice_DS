from math import radians, cos, sin, asin, sqrt

import numpy as np
import pandas as pd

stations_path = r"C:\Users\rolny\Desktop\Shiro\lecture01\data\hubway_stations.csv"

trips_path = r"C:\Users\rolny\Desktop\Shiro\lecture01\data\hubway_trips.csv"

def haversine(pt, lat2=42.355589, lon2=-71.060175):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)

    pt = [longitude, latitude]
    """
    lon1 = pt[0]
    lat1 = pt[1]

    # convert decimal degrees to radians (chuyển từ số thập phân sang đơn vị radian)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles
    return c * r


def get_distance():
    # Read the data from the file "hubway_stations.csv"
    stations = pd.read_csv(stations_path)

    # Read the data from the file "hubway_trips.csv"
    trips = pd.read_csv(trips_path)

    station_counts = np.unique(trips['strt_statn'].dropna(), return_counts=True) # đếm số lần xuất hiện của mỗi mã trạm trong cột 'strt_statn' của dataframe trips, bỏ qua các giá trị NaN
    counts_df = pd.DataFrame({'id': station_counts[0], 'checkouts': station_counts[1]}) # tạo một dataframe mới gồm cột mã trạm và số lần xuất hiện của mã
    counts_df = counts_df.join(stations.set_index('id'), on='id') # nối dF counts_df với dF stations dựa trên cột 'id' để thêm thông tin về trạm vào counts_df
    # add to the pandas dataframe the distance using the function we defined above and using map 
    counts_df.loc[:, 'dist_to_center'] = list(map(haversine, counts_df[['lng', 'lat']].values)) #tính khoảng cách từ mỗi trạm đến trung tâm bằng hàm haversine , thêm kết quả vào cột 'dist_to_center' của counts_df
    ''' hàm loc lấy ra 1 hàng và 1 cột được chỉ định, dùng ':' để lấy tất cả hàng, 
    'dist_to_center' chưa có trong count_df nên sẽ tạo thành một cột mới của dF '''
    return counts_df
