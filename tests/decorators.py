from tempfile import NamedTemporaryFile

import pytest

from decorators import log


def test_log_success():
    """Тест успешного выполнения"""
    with NamedTemporaryFile() as tmp:

        @log(filename=tmp.name)
        def my_func(a, b):
            return a + b

        my_func(1, 2)

        with open(tmp.name, "r") as f:
            assert f.read().strip() == "my_func ok"


def test_log_error():
    """Тест ошибки"""
    with NamedTemporaryFile() as tmp:

        @log(filename=tmp.name)
        def my_func(a, b):
            raise RuntimeError("error")

        with pytest.raises(RuntimeError):
            my_func(1, 2)

        with open(tmp.name, "r") as f:
            assert f.read().strip() == "my_func error: RuntimeError. Inputs: (1, 2), {}"


def test_log_console_basic(capsys):
    """Тест консольного вывода"""

    @log()
    def test_func():
        return "ok"

    test_func()
    assert capsys.readouterr().out.strip() == "test_func ok"


def test_log_different_error_types():
    """Тестируем разные типы ошибок"""
    error_types = [ValueError, TypeError, RuntimeError, ZeroDivisionError]

    for error_type in error_types:
        with NamedTemporaryFile() as tmp:

            @log(filename=tmp.name)
            def my_func():
                raise error_type("test")

            with pytest.raises(error_type):
                my_func()

            with open(tmp.name, "r") as f:
                content = f.read().strip()
                assert content == f"my_func error: {error_type.__name__}. Inputs: (), {{}}"
