import os
import pytest

from modules.shared.environ.infraestructure import PyEnviron


CONTENT = """
STR_VALUE=str_value
STR_VALUE_1=1
INT_VALUE=1
BOOL_VALUE=True
BOOL_VALUE_1=1
"""


@pytest.fixture(scope="session")
def env_file(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("tmp")
    app_dir = tmp_dir / "app"
    app_dir.mkdir()
    (app_dir / ".env").write_text(CONTENT, "utf-8")
    return tmp_dir


def test_non_existent_value(env_file):
    path = os.path.join(env_file, "app", ".env")
    py_environ = PyEnviron(path)
    assert py_environ.get_str("NON-EXISTENT") is None


def test_get_value_as_str(env_file):
    path = os.path.join(env_file, "app", ".env")
    py_environ = PyEnviron(path)
    assert py_environ.get_str("STR_VALUE") == "str_value"
    assert py_environ.get_str("STR_VALUE_1") == "1"


def test_get_value_as_int(env_file):
    path = os.path.join(env_file, "app", ".env")
    py_environ = PyEnviron(path)
    assert py_environ.get_int("INT_VALUE") == 1


def test_get_value_as_bool(env_file):
    path = os.path.join(env_file, "app", ".env")
    py_environ = PyEnviron(path)
    assert py_environ.get_bool("BOOL_VALUE") is True
    assert py_environ.get_bool("BOOL_VALUE_1") is True
