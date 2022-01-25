from pytest import raises
from unittest.mock import Mock
import sys
import py_unittest_tools.imports as test_module
import numpy as np


def test_mock_imports_none():
    copy = sys.modules.copy()

    with test_module.mock_imports():
        assert sys.modules == copy

    assert sys.modules == copy


def test_mock_imports_none_exception():
    with raises(ValueError):
        with test_module.mock_imports():
            ve = ValueError()
            raise ve


def test_mock_imports_unloads():
    import datetime as dt

    with test_module.mock_imports(unload='datetime'):
        assert 'datetime' not in sys.modules
        import datetime as dt2
        assert 'datetime' in sys.modules
        assert dt is not dt2

    assert 'datetime' in sys.modules
    import datetime as dt3
    assert dt is dt3

    with test_module.mock_imports(unload=['datetime']):
        assert 'datetime' not in sys.modules
        import datetime as dt4
        assert 'datetime' in sys.modules
        assert dt is not dt4


def test_mock_imports_mocks():
    mock_module = Mock()
    with test_module.mock_imports(mock={
        'a': mock_module
    }):
        assert sys.modules['a'] is mock_module
        import a
        assert a is mock_module

    assert 'a' not in sys.modules


def test_mock_imports_fails():
    import datetime as dt

    with test_module.mock_imports(fail='b'):
        assert 'b' not in sys.modules

        with raises(ImportError):
            import b

        assert 'b' not in sys.modules

    with test_module.mock_imports(fail=['b']):
        assert 'b' not in sys.modules

        with raises(ImportError):
            import b

        assert 'b' not in sys.modules


def test_mock_imports_fails_hack_rm_raiser():
    import sys

    with test_module.mock_imports(fail='b'):
        assert isinstance(sys.meta_path[0], test_module.ImportRaiser)
        assert sys.meta_path[0].fail_modules == {'b'}
        del sys.meta_path[0]


def test_ImportRaiser___init__():
    R = test_module.ImportRaiser('a', 'b', 'c')
    assert R.fail_modules == {'a', 'b', 'c'}


def test_ImportRaiser_find_spec():
    R = test_module.ImportRaiser('a', 'b', 'c')

    with raises(ImportError):
        R.find_spec('a', 'path/to/module')

    with raises(ImportError):
        R.find_spec('b', 'path/to/module')

    with raises(ImportError):
        R.find_spec('c', 'path/to/module')

    R.find_spec('d', 'path/to/module')
