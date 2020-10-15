import typing as tp
import itertools as it
import numpy as np
from static_frame.core.util import DtypeSpecifier
from static_frame.core.container import ContainerOperand

import static_frame as sf
import function_pipe as fpn
# from function_pipe import pipe_node
# from function_pipe import pipe_node_factory

DtypeSpecOrSpecs = tp.Union[DtypeSpecifier, tp.Tuple[DtypeSpecifier, ...]]
DTYPE_OBJECT = np.dtype(object)

def dtype_to_element_iter(dtype: np.dtype) -> tp.Iterator[tp.Any]:

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


def dtype_to_array(
        dtype: np.dtype,
        count: int,
        gen: tp.Optional[tp.Iterator[tp.Any]] = None,
        ) -> np.ndarray:
    '''
    Args:
        gen: optionally supply a generator of values, to e used instead
    '''
    if not gen:
        gen = dtype_to_element_iter(dtype)

    if dtype.kind != 'O':
        array = np.fromiter(gen, count=count, dtype=dtype)
    else:
        array = np.empty(shape=count, dtype=dtype) # object
        for i, v in zip(range(len(array)), gen):
            array[i] = v

    array.flags.writeable = False
    return array


def dtype_spec_to_array(
        dtype_spec: DtypeSpecOrSpecs,
        count: int,
        ) -> np.ndarray:

    if isinstance(dtype_spec, tuple):
        # an object type of tuples
        gen = zip(*(dtype_to_element_iter(np.dtype(dts)) for dts in dtype_spec))
        return dtype_to_array(DTYPE_OBJECT, count=count, gen=gen)

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


class Builder:

    @staticmethod
    def build_index(
            count: int,
            constructor: tp.Type[ContainerOperand],
            dtype_spec: DtypeSpecOrSpecs,
            index_constructors=None,
            ) -> tp.Union[sf.Index, sf.IndexHierarchy]:

        if issubclass(constructor, IH):
            # dtype_spec must be a tuple
            if not isinstance(dtype_spec, tuple) or len(dtype_spec) < 2:
                raise RuntimeError(f'for building IH dtype_spec must be a tuple')
            if index_constructors and len(index_constructors) != len(dtype_spec):
                raise RuntimeError(f'length of index_constructors must be the same as dtype_spec')
            tb = sf.TypeBlocks.from_blocks(dtype_spec_to_array(dts, count=count)
                    for dts in dtype_spec)
            return constructor._from_type_blocks(tb,
                    index_constructors=index_constructors,
                    own_blocks=True,
                    )

        if index_constructors:
            raise RuntimeError('cannot provide index_constructors if not building an IH index')

        array = dtype_spec_to_array(dtype_spec, count=count)
        return constructor.from_labels(array)






@fpn.pipe_node_factory
def f(constructor, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['f'] = dict(constructor=constructor)

@fpn.pipe_node_factory
def i(constructor,
        dtype_spec: DtypeSpecOrSpecs,
        index_constructors=None,
        **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['i'] = dict(constructor=constructor,
            dtype_spec=dtype_spec,
            index_constructors=index_constructors,
            )

@fpn.pipe_node_factory
def c(constructor,
            dtype_spec: DtypeSpecOrSpecs,
            index_constructors=None,
            **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['c'] = dict(constructor=constructor,
            dtype_spec=dtype_spec,
            index_constructors=index_constructors,
            )

@fpn.pipe_node_factory
def v(*dtype_spec, **kwargs):
    pni = kwargs[fpn.PN_INPUT]
    pni['v'] = dict(dtype_spec=dtype_spec)


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
