from rp2 import hagai_2018, load_one_to_one_mouse_orthologues, load_biomart_gene_symbols_df


class Analysis:
    def __init__(self, species, gene_ids, orthologues_df=None):
        self._condition_columns = ["replicate", "treatment", "time_point"]
        self._species = species
        self._gene_ids = gene_ids
        self._orthologues_df = orthologues_df

    @property
    def condition_columns(self):
        return self._condition_columns

    @property
    def index_columns(self):
        return ["gene"] + self._condition_columns

    @property
    def species(self):
        return self._species

    @property
    def gene_ids(self):
        return self._gene_ids

    def create_orthologue_analysis(self, species):
        if species == self._species:
            return self

        if self._orthologues_df is None:
            self._orthologues_df = load_one_to_one_mouse_orthologues().reset_index()

        gene_mask = self._orthologues_df[f"{self._species}_gene"].isin(self._gene_ids)
        orthologue_gene_ids = self._orthologues_df.loc[gene_mask, f"{species}_gene"].to_list()
        return Analysis(species, orthologue_gene_ids, self._orthologues_df)


def create_default_mouse_analysis():
    additional_gene_symbols = ["Il1b", "Tnf"]

    gene_info_df = load_biomart_gene_symbols_df("mouse")
    additional_gens_ids = gene_info_df.loc[gene_info_df.symbol.isin(additional_gene_symbols)].index

    lps_responsive_genes = hagai_2018.load_lps_responsive_genes()
    analysis_gene_ids = sorted(set(additional_gens_ids).union(lps_responsive_genes))

    return Analysis("mouse", analysis_gene_ids)
