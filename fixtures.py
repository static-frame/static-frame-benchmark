import typing as tp
import itertools as it
import numpy as np
from static_frame.core.util import DtypeSpecifier


def dtype_spec_to_element(dtype: np.dtype) -> tp.Iterator[tp.Any]:

    if dtype.kind == 'i': # int
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'u': # int unsigned
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'f': # float
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'c': # complex
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'b': # boolean
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind in ('U', 'S'): # str
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'O': # object
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'M': # datetime64
        return it.cycle((0, -100, 25, -85555555, 23485))
    elif dtype.kind == 'm': # timedelta64
        return it.cycle((0, -100, 25, -85555555, 23485))

    raise NotImplementedError()