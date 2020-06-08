import shutil
import urllib.parse
import urllib.request
import contextlib
import os
from pathlib import Path


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

        if df.index.name == map_key:
            insert_index = 0
            symbols = self._mapping_series[df.index]
        else:
            insert_index = df.columns.get_loc(map_key) + 1
            symbols = df[map_key].map(self._mapping_series)

        df.insert(insert_index, "gene_symbol", symbols)

        return df
