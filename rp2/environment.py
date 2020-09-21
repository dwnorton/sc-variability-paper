import sys


def make_semver(version_string):
    components = [int(v) for v in version_string.split(".")]
    if len(components) != 3:
        raise ValueError(f"Invalid version ({version_string})")
    return components


def get_python_version():
    return sys.version.split()[0]


def get_package_version(package):
    m = __import__(package)
    version = m.__version__
    return version


def check_environment():
    min_seaborn_version = "0.10.1"
    try:
        required_version = make_semver(min_seaborn_version)
        actual_version_str = get_package_version("seaborn")
        actual_version = make_semver(actual_version_str)
        if actual_version < required_version:
            raise ValueError(f"Dependency >={min_seaborn_version} not satisfied by {actual_version_str}")
    except Exception:
        print("Your Python environment does not contain the required dependencies.")
        print("Check README.md for details of configuring a Python environment.")
        raise Exception(f"seaborn package version >={min_seaborn_version} not installed")
