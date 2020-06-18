import shutil
import urllib.parse
import urllib.request
import contextlib
import os
from pathlib import Path

import pandas as pd

from rp2.paths import get_data_path


def create_folder(path, create_clean=False):
    path = Path(path)
    if create_clean and path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def get_url_filename(url):
    return Path(urllib.parse.urlparse(url).path).name


def download_file(url, to_dir, rename_to=None):
    to_dir = Path(to_dir)
    filename = get_url_filename(url) if rename_to is None else rename_to
    dst = to_dir.joinpath(filename)
    create_folder(to_dir)
    return urllib.request.urlretrieve(url, dst)[0]


def fetch_file(url, to_dir, rename_to=None):
    to_dir = Path(to_dir)
    filename = get_url_filename(url) if rename_to is None else rename_to
    filepath = to_dir.joinpath(filename)
    if not filepath.exists():
        download_file(url, to_dir=to_dir, rename_to=rename_to)

    return filepath


@contextlib.contextmanager
def working_directory(path):
    prev_wd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_wd)


class GeneSymbolMap:
    def __init__(self, mapping_df):
        self._mapping_series = mapping_df.symbol

    def lookup(self, gene_id):
        return self._mapping_series[gene_id]

    def added_to(self, df, map_key="gene"):
        df = df.copy()
        self.add_to(df, map_key=map_key)
        return df

    def add_to(self, df, map_key="gene"):
        if df.index.name == map_key:
            insert_index = 0
            symbols = self._mapping_series[df.index]
        else:
            insert_index = df.columns.get_loc(map_key) + 1
            symbols = df[map_key].map(self._mapping_series)

        df.insert(insert_index, "gene_symbol", symbols)


def load_biomart_gene_symbols_df(species):
    return pd.read_table(
        get_data_path("BioMart", f"{species}_genes.tsv"),
        names=["id", "symbol", "description"],
        index_col=0
    )


def create_gene_symbol_map(species):
    gene_symbols_df = load_biomart_gene_symbols_df(species)
    return GeneSymbolMap(gene_symbols_df)


def check_environment():
    def make_semver(version_string):
        components = [int(v) for v in version_string.split(".")]
        if len(components) != 3:
            raise ValueError(f"Invalid version ({version_string})")
        return components

    min_seaborn_version = "0.10.1"
    try:
        import seaborn
        required_version = make_semver(min_seaborn_version)
        actual_version_str = seaborn.__version__
        actual_version = make_semver(actual_version_str)
        if actual_version < required_version:
            raise ValueError(f"Dependency >={min_seaborn_version} not satisfied by {actual_version_str}")
    except Exception:
        print("Your Python environment does not contain the required dependencies.")
        print("Check README.md for details of configuring a Python environment.")
        raise Exception(f"seaborn package version >={min_seaborn_version} not installed")
