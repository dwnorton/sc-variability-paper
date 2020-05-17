import urllib.parse
import urllib.request
from pathlib import Path


data_path = Path(__file__).parent.parent.joinpath("Data")


def get_data_path(*names):
    return data_path.joinpath(*names)


def get_url_filename(url):
    return Path(urllib.parse.urlparse(url).path).name


def download_file(url, to_dir, rename_to=None):
    to_dir = Path(to_dir)
    filename = get_url_filename(url) if rename_to is None else rename_to
    dst = to_dir.joinpath(filename)
    to_dir.mkdir(parents=True, exist_ok=True)
    return urllib.request.urlretrieve(url, dst)[0]


def fetch_file(url, to_dir, rename_to=None):
    to_dir = Path(to_dir)
    filename = get_url_filename(url) if rename_to is None else rename_to
    filepath = to_dir.joinpath(filename)
    if not filepath.exists():
        download_file(url, to_dir=to_dir, rename_to=rename_to)

    return filepath
