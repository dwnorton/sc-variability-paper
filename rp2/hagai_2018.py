import functools

import anndata
import numpy as np
import pandas as pd
from scipy import stats

from rp2.paths import get_data_path


def load_st4_phagocyte_fc_divergence():
    return pd.read_excel(
        get_data_path("hagai_2018", "41586_2018_657_MOESM4_ESM.xlsx"),
        sheet_name="phagocytes_FC_diveregnce"
    )


def load_lps_responsive_genes(species="mouse", max_padj=0.01):
    fc_divergence_df = load_st4_phagocyte_fc_divergence()
    return fc_divergence_df.loc[fc_divergence_df[f"{species}_padj"] < max_padj].gene


def load_umi_count(species):
    return anndata.read_h5ad(get_data_path("ArrayExpress", f"E-MTAB-6754.processed.2.{species}.h5ad"))


def calculate_umi_subset_condition_stats(umi_count_ad, obs_subset):
    umi_subset = umi_count_ad[obs_subset.index, :]
    umi_matrix = umi_subset.X.A
    return pd.DataFrame(
        index=pd.Index(umi_subset.var_names, name="gene"),
        data={
            "n_barcodes": len(obs_subset),
            "min": np.min(umi_matrix, axis=0),
            "max": np.max(umi_matrix, axis=0),
            "mean": np.mean(umi_matrix, axis=0),
            "variance": np.var(umi_matrix, ddof=1, axis=0),
            "std_dev": np.std(umi_matrix, ddof=1, axis=0),
            "skew": stats.skew(umi_matrix, axis=0),
        }
    )


def calculate_umi_condition_stats(umi_count_ad, group_columns=None, sort_columns=None):
    group_columns = group_columns or ["replicate", "treatment", "time_point"]
    sort_columns = sort_columns or ["gene", "replicate", "time_point", "treatment"]

    stats_fun = functools.partial(calculate_umi_subset_condition_stats, umi_count_ad)
    condition_stats_df = umi_count_ad.obs.groupby(group_columns).apply(stats_fun)
    condition_stats_df = condition_stats_df.sort_values(sort_columns)
    condition_stats_df = condition_stats_df.reset_index()

    column_order = ["gene"] + [c for c in condition_stats_df.columns if c != "gene"]
    return condition_stats_df.loc[:, column_order]
