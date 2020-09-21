from rp2 import create_folder
from rp2.environment import check_environment
from rp2.paths import get_output_path


schema_version = 5


def make_intermediate_folder_name(nb_name):
    return f"{nb_name}.{schema_version}"


class NotebookDependencyError(Exception):
    pass


class NotebookDependency:
    def __init__(self, name, data_path):
        self._name = name
        self._data_path = data_path

    def access_path(self, *names):
        path = self._data_path.joinpath(*names)
        if not path.exists():
            raise NotebookDependencyError(f'Content from "{self._name}" is missing: ensure the notebook has been executed')
        return path


class NotebookEnvironment:
    def __init__(self, intermediate_path):
        self._intermediate_path = intermediate_path

    def get_intermediate_path(self, *names):
        return self._intermediate_path.joinpath(*names)


def initialise_environment(nb_name, dependencies=None):
    check_environment()

    root_path = get_output_path(".intermediate")

    dependency_list = []
    if dependencies is not None:
        for dependency_name in dependencies:
            dependency_path = root_path.joinpath(make_intermediate_folder_name(dependency_name))
            if not dependency_path.is_dir():
                raise NotebookDependencyError(f'Please execute notebook "{dependency_name}" prior to running this one')
            dependency_list.append(NotebookDependency(nb_name, dependency_path))

    intermediate_path = root_path.joinpath(make_intermediate_folder_name(nb_name))
    create_folder(intermediate_path, create_clean=True)

    nb_env = NotebookEnvironment(intermediate_path)
    return nb_env if dependencies is None else [nb_env] + dependency_list
