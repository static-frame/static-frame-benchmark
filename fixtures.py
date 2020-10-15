import typing as tp
import itertools as it
import numpy as np
from static_frame.core.util import DtypeSpecifier
import static_frame as sf
import function_pipe as fpn
# from function_pipe import pipe_node
# from function_pipe import pipe_node_factory


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


def dtype_to_array(dtype: np.dtype, count: int) -> np.ndarray:
    gen = dtype_to_element(dtype)
    if dtype.kind != 'O':
        return np.fromiter(gen, count=count, dtype=dtype)

    array = np.empty(shape=count, dtype=dtype) # object
    for i, v in zip(range(len(array)), gen):
        array[i] = v

    return array


def dtype_spec_to_array(
        dtype_spec: DtypeSpecifier,
        count: int,
        ) -> np.ndarray:
    dtype = np.dtype(dtype_spec)
    return dtype_to_array(dtype, count)


F = sf.Frame
FG = sf.FrameGO
I = sf.Index
IG = sf.IndexGO
IH = sf.IndexHierarchy
IHG = sf.IndexHierarchyGO
ID = sf.IndexDate
IDG = sf.IndexDateGO
IN = sf.IndexNanosecond
ING = sf.IndexNanosecondGO


@fpn.pipe_node_factory
def f(type_symbol, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['f'] = dict(type_symbol=type_symbol)

@fpn.pipe_node_factory
def i(type_symbol, values_dtype_spec, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['i'] = dict(type_symbol=type_symbol, values_dtype_spec=values_dtype_spec)

@fpn.pipe_node_factory
def c(type_symbol, values_dtype_spec, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['c'] = dict(type_symbol=type_symbol, values_dtype_spec=values_dtype_spec)

@fpn.pipe_node_factory
def v(*values_dtype_spec, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['v'] = dict(values_dtype_spec=values_dtype_spec)


class Shape(fpn.PipeNodeInput):
    def __init__(self, shape: tp.Tuple[int, int]):
        self.shape = shape
        self.ref = dict()

    def __setitem__(self, key, value):
        if key in self.ref:
            raise KeyError('duplicate key', key)
        self.ref[key] = value

    def __repr__(self) -> str:
        return repr(self.ref)
