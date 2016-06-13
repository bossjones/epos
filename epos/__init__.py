from __future__ import absolute_import, division, print_function

from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(relativeCreated)6d %(threadName)s %(message)s')


@contextmanager
def ignoring(*exceptions):
    try:
        yield
    except exceptions:
        pass


from dask import delayed
from functools import partial

with ignoring(ImportError):
    from dask_mesos import mesos, MesosExecutor

with ignoring(ImportError):
    from .context import Lock, Persist

with ignoring(ImportError):
    from .spark import spark


from .odo import odo
from .chronos import chronos
from .marathon import marathon
