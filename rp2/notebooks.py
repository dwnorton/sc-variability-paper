from rp2 import check_environment, create_folder
from rp2.paths import get_output_path


class NotebookDependencyError(Exception):
    pass


class NotebookDependency:
    def __init__(self, name, data_path):
        self._name = name
        self._data_path = data_path

    def access_path(self, *names):
        path = self._data_path.joinpath(*names)
        if not path.exists():
            raise NotebookDependencyError(f'Content missing from "{self._name}" - ensure the notebook has been executed')
        return path


class NotebookEnvironment:
    def __init__(self, intermediate_path):
        self._intermediate_path = intermediate_path

    def register_dependency(self, nb_name):
        root_path = self._intermediate_path.parent
        nb_intermediate_path = root_path.joinpath(nb_name)
        if not nb_intermediate_path.is_dir():
            raise NotebookDependencyError(f'Please execute notebook "{nb_name}" prior to running this one')

        return NotebookDependency(nb_name, nb_intermediate_path)

    def get_intermediate_path(self, *names):
        return self._intermediate_path.joinpath(*names)


def initialise_environment(nb_name):
    check_environment()

    intermediate_path = get_output_path(".intermediate", nb_name)
    create_folder(intermediate_path, create_clean=True)

    return NotebookEnvironment(intermediate_path)
