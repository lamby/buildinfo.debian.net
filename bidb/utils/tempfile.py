from __future__ import absolute_import

import shutil
import tempfile
import contextlib

@contextlib.contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()

    try:
        yield name
    finally:
        shutil.rmtree(name, ignore_errors=True)
