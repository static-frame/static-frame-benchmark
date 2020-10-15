import typing as tp
import itertools as it
import numpy as np
from static_frame.core.util import DtypeSpecifier


def dtype_to_element(dtype: np.dtype) -> tp.Iterator[tp.Any]:

    if dtype.kind == 'i': # int
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'u': # int unsigned
        return it.cycle((0, 100, 25, 512, 234))
    elif dtype.kind == 'f': # float
        return it.cycle((0.0, 3.2, 3.2e-8, np.nan))
    elif dtype.kind == 'c': # complex
        return it.cycle((3+5j, np.nan+3j, 100+.0003j))
    elif dtype.kind == 'b': # boolean
        return it.cycle((False, True))
    elif dtype.kind in ('U', 'S'): # str
        return it.cycle(('foo', 'foo', 'bar', 'baz'))
    elif dtype.kind == 'O': # object
        return it.cycle((None, 'foo', 2.5, False))
    elif dtype.kind == 'M': # datetime64
        return it.cycle((np.datetime64('2012-01-05'), np.datetime64('2015-02-20'), ))
    elif dtype.kind == 'm': # timedelta64
        return it.cycle((np.timedelta64(3), np.timedelta64(20),))

    raise NotImplementedError(f'no handling for {dtype}')


def dtype_to_array(dtype: np.dtype, size: int) -> np.ndarray:
    if dtype.kind != 'O':
        return np.fromiter(dtype_to_element(dtype), size=size, dtype=dtype)