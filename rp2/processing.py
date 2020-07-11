import numpy as np
import pandas as pd
from scipy import linalg, spatial


def calculate_mahalanobis_distance(values):
    centroid = np.mean(values, axis=0)
    cov_mtx = np.cov(values, rowvar=False)
    inv_cov_mtx = linalg.inv(cov_mtx)
    distances = [spatial.distance.mahalanobis(row, centroid, inv_cov_mtx)
                 for row in values]
    return distances


def calculate_df_mahalanobis_distance(df, columns, name="distance"):
    values = df.loc[:, columns].to_numpy()
    distances = calculate_mahalanobis_distance(values)

    return pd.DataFrame(index=df.index, data={name: distances})
