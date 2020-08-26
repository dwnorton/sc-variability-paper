import numpy as np
import pandas as pd
from scipy import linalg, spatial, stats


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


def calculate_df_pearson_r(df, x_var, y_var):
    cr, cp = stats.pearsonr(df[x_var], df[y_var])
    return pd.Series(data={"r": cr, "r_pval": cp})


def calculate_df_spearman_r(df, x_var, y_var):
    sp_corr = stats.spearmanr(df[x_var], df[y_var])
    return pd.Series(data={"r": sp_corr.correlation, "r_pval": sp_corr.pvalue})
