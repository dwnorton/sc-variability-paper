from rp2 import hagai_2018, load_mouse_orthologues, load_biomart_gene_symbols_df


class Analysis:
    def __init__(self, mouse_gene_ids):
        self._mouse_gene_ids = mouse_gene_ids
        self._orthologues_df = None

    @property
    def condition_columns(self):
        return ["replicate", "treatment", "time_point"]

    @property
    def mouse_gene_ids(self):
        return self._mouse_gene_ids

    def get_orthologue_gene_ids(self, species):
        if self._orthologues_df is None:
            self._orthologues_df = load_mouse_orthologues()
        return self._orthologues_df.loc[self._orthologues_df.index.isin(self._mouse_gene_ids), f"{species}_gene"]


def create_default_analysis():
    additional_gene_symbols = ["Il1b", "Tnf"]

    gene_info_df = load_biomart_gene_symbols_df("mouse")
    additional_gens_ids = gene_info_df.loc[gene_info_df.symbol.isin(additional_gene_symbols)].index

    lps_responsive_genes = hagai_2018.load_lps_responsive_genes()
    analysis_gene_ids = sorted(set(additional_gens_ids).union(lps_responsive_genes))

    return Analysis(analysis_gene_ids)
