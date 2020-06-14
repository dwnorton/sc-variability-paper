import anndata
import pandas as pd

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
