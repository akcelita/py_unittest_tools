from typing import List, Mapping, Any
import sys
import contextlib


@contextlib.contextmanager
def mock_imports(
    mock:Mapping[str, Any] = None,
    unload:List[str] = None,
    fail:List[str] = None,
):
    """Mocks the python module import mechanism within a given context and restores it on exit.
        Parameters
        ==========
        mock: List[str] - mock modules to add to python's module cache.
        unload: List[str] - modules to remove from python's import mechanism.
        fail: List[str] - modules that will fail to import within the context.
    """

    if unload is not None and isinstance(unload, str):
        unload = [unload]

    if fail is not None and isinstance(fail, str):
        fail = [fail]

    exc = None
    sys_modules_clone = sys.modules.copy()

    if fail:
        raiser = ImportRaiser(*fail)
        sys.meta_path.insert(0, raiser)

    for name in (
        n
        for l in [unload, fail]
        if l
        for n in l
        if n in sys.modules
    ):
        del sys.modules[name]

    for name, module in (mock or {}).items():
        sys.modules[name] = module

    try:
        yield
    except Exception as _exc:
        exc = _exc


    for name, module in sys_modules_clone.items():
        sys.modules[name] = module

    for name in list(sys.modules.keys()):
        if name not in sys_modules_clone:
            del sys.modules[name]

    if fail:
        try:
            sys.meta_path.remove(raiser)
        except ValueError:
            pass

    if exc:
        raise exc


class ImportRaiser:
    def __init__(self, *fail_modules):
        self.fail_modules = set(fail_modules)

    def find_spec(self, fullname, path, target=None):
        if fullname in self.fail_modules:
           # we get here if the module is not loaded and not in sys.modules
            raise ImportError("Programatic Import Fail of module {}".format(fullname))
