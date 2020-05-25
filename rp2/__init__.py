import shutil
import urllib.parse
import urllib.request
import contextlib
import os
from pathlib import Path


data_path = Path(__file__).parent.parent.joinpath("Data")
output_path = Path(__file__).parent.parent.joinpath("Output")
scripts_path = Path(__file__).parent.parent.joinpath("Scripts")


def get_data_path(*names):
    return data_path.joinpath(*names)


def get_output_path(*names):
    return output_path.joinpath(*names)


def get_scripts_path(*names):
    return scripts_path.joinpath(*names)


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
