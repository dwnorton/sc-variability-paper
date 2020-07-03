import functools

import anndata
import numpy as np
import pandas as pd
import scanpy
from scipy import stats

from rp2 import load_biomart_gene_symbols_df, create_normalised_adata
from rp2.paths import get_data_path


def load_st4_phagocyte_fc_divergence():
    return pd.read_excel(
        get_data_path("hagai_2018", "41586_2018_657_MOESM4_ESM.xlsx"),
        sheet_name="phagocytes_FC_diveregnce"
    )


def load_lps_responsive_genes(species="mouse", max_padj=0.01):
    fc_divergence_df = load_st4_phagocyte_fc_divergence()
    return fc_divergence_df.loc[fc_divergence_df[f"{species}_padj"] < max_padj].gene


def load_umi_counts(species):
    return anndata.read_h5ad(get_data_path("ArrayExpress", f"E-MTAB-6754.processed.2.{species}.h5ad"))


def load_umi_counts_with_additional_annotation(species):
    umi_counts_adata = load_umi_counts(species)

    gene_info_df = load_biomart_gene_symbols_df(species)
    umi_counts_adata.var["symbol"] = gene_info_df.loc[umi_counts_adata.var_names, "symbol"]

    lps_responsive_ids = load_lps_responsive_genes()
    umi_counts_adata.var["lps_responsive"] = umi_counts_adata.var_names.isin(lps_responsive_ids)

    return umi_counts_adata


def load_counts(species, scaling="umi"):
    scaling_functions = {
        "umi": lambda a: a,
        "cpt": lambda a: create_normalised_adata(a, 1e3),
        "cpm": lambda a: create_normalised_adata(a, 1e6),
        "median": lambda a: create_normalised_adata(a, None),
    }

    if not isinstance(scaling, list):
        scaling = [scaling]

    umi_counts_adata = load_umi_counts_with_additional_annotation(species)
    scanpy.pp.filter_genes(umi_counts_adata, min_counts=1)

    results = [scaling_functions[s](umi_counts_adata) for s in scaling]

    return results if len(results) > 1 else results[0]


def calculate_counts_subset_condition_stats(umi_count_ad, obs_subset):
    counts_subset = umi_count_ad[obs_subset.index, :]
    counts_matrix = counts_subset.X.A
    return pd.DataFrame(
        index=pd.Index(counts_subset.var_names, name="gene"),
        data={
            "n_barcodes": len(obs_subset),
            "min": np.min(counts_matrix, axis=0),
            "max": np.max(counts_matrix, axis=0),
            "mean": np.mean(counts_matrix, axis=0),
            "variance": np.var(counts_matrix, ddof=1, axis=0),
            "std_dev": np.std(counts_matrix, ddof=1, axis=0),
            "skew": stats.skew(counts_matrix, axis=0),
        }
    )


def calculate_counts_condition_stats(counts_adata, group_columns=None, sort_columns=None):
    group_columns = group_columns or ["replicate", "treatment", "time_point"]
    sort_columns = sort_columns or ["gene", "replicate", "time_point", "treatment"]

    stats_fun = functools.partial(calculate_counts_subset_condition_stats, counts_adata)
    condition_stats_df = counts_adata.obs.groupby(group_columns).apply(stats_fun)
    condition_stats_df = condition_stats_df.sort_values(sort_columns)
    condition_stats_df = condition_stats_df.reset_index()

    column_order = ["gene"] + [c for c in condition_stats_df.columns if c != "gene"]
    return condition_stats_df.loc[:, column_order]
