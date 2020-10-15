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

#-------------------------------------------------------------------------------
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
        return it.cycle(('foo', 'bar', 'baz'))
    elif dtype.kind == 'O': # object
        return it.cycle((None, 'foo', 2.5, False))
    elif dtype.kind == 'M': # datetime64
        return it.cycle((np.datetime64('2012-01-05'), np.datetime64('2015-02-20'), ))
    elif dtype.kind == 'm': # timedelta64
        return it.cycle((np.timedelta64(3), np.timedelta64(20),))

    raise NotImplementedError(f'no handling for {dtype}')


DTYPE_KINDS_NO_FROMITER = ('O', 'U', 'S')

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

    if dtype.kind not in DTYPE_KINDS_NO_FROMITER:
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



#-------------------------------------------------------------------------------
F = sf.Frame
Fg = sf.FrameGO
I = sf.Index
Ig = sf.IndexGO
IH = sf.IndexHierarchy
IHg = sf.IndexHierarchyGO

IY = sf.IndexYear
IYg = sf.IndexYearGO
IYM = sf.IndexYearMonth
IYMg = sf.IndexYearMonthGO
ID = sf.IndexDate
IDg = sf.IndexDateGO
IS = sf.IndexSecond
ISg = sf.IndexSecondGO
IN = sf.IndexNanosecond
INg = sf.IndexNanosecondGO

dtY = np.dtype('datetime64[Y]')
dtM = np.dtype('datetime64[M]')
dtD = np.dtype('datetime64[D]')
# NOTE: we not do hour as IH is ambiguous
dts = np.dtype('datetime64[s]')
dtns = np.dtype('datetime64[ns]')

#-------------------------------------------------------------------------------
ConstructorOrConstructors = tp.Union[
        tp.Type[ContainerOperand],
        tp.Tuple[tp.Type[ContainerOperand], ...]
        ]
ShapeType = tp.Tuple[int, int]
IndexTypes = tp.Union[sf.Index, sf.IndexHierarchy]

class Builder:

    @staticmethod
    def build_index(
            count: int,
            constructor: ConstructorOrConstructors,
            dtype_spec: DtypeSpecOrSpecs,
            ) -> IndexTypes:

        if isinstance(constructor, tuple):
            # dtype_spec must be a tuple
            if not isinstance(dtype_spec, tuple) or len(dtype_spec) < 2:
                raise RuntimeError(f'for building IH dtype_spec must be a tuple')
            if len(constructor) != len(dtype_spec):
                raise RuntimeError(f'length of index_constructors must be the same as dtype_spec')

            is_static = {c.STATIC for c in constructor}
            assert len(is_static) == 1

            cls = (sf.IndexHierarchy if is_static.pop()
                    else sf.IndexHierarchyGO)

            tb = sf.TypeBlocks.from_blocks(dtype_spec_to_array(dts, count=count)
                    for dts in dtype_spec)

            return cls._from_type_blocks(tb,
                    index_constructors=constructor,
                    own_blocks=True,
                    )

        # if constructor is IndexHierarchy, this will work, as array will be a 1D array of tuples that, when given to from_labels, will work
        array = dtype_spec_to_array(dtype_spec, count=count)
        return constructor.from_labels(array)

    @staticmethod
    def build_values(
            shape: ShapeType,
            dtype_specs: tp.Sequence[DtypeSpecOrSpecs]
            ) -> sf.TypeBlocks:

        count_row, count_col = shape
        count_dtype = len(dtype_specs)

        def gen() -> tp.Iterator[np.ndarray]:
            for col in range(count_col):
                yield dtype_spec_to_array(
                        dtype_specs[col % count_dtype],
                        count=count_row,
                        )
        return sf.TypeBlocks.from_blocks(gen())


    @staticmethod
    def build_frame(index, columns, blocks, constructor) -> sf.Frame:
        return constructor(blocks,
                index=index,
                columns=columns,
                own_data=True,
                own_index=True,
                own_columns=True,
                )

#-------------------------------------------------------------------------------
from functools import partial
pipe_node_factory = partial(fpn.pipe_node_factory, core_decorator=lambda f: f)

@pipe_node_factory
@fpn.pipe_kwarg_bind(fpn.PN_INPUT)
def f(pni, constructor):
    # pni = kwargs[fpn.PN_INPUT]
    pni['f'] = dict(constructor=constructor)
    if pni.complete():
        return pni.build()

@pipe_node_factory
@fpn.pipe_kwarg_bind(fpn.PN_INPUT)
def i(pni,
        constructor,
        dtype_spec: DtypeSpecOrSpecs,
        ):
    pni['i'] = dict(constructor=constructor, dtype_spec=dtype_spec)
    if pni.complete():
        return pni.build()

@pipe_node_factory
@fpn.pipe_kwarg_bind(fpn.PN_INPUT)
def c(pni,
        constructor,
        dtype_spec: DtypeSpecOrSpecs,
        ):
    pni['c'] = dict(constructor=constructor, dtype_spec=dtype_spec)
    if pni.complete():
        return pni.build()

@pipe_node_factory
@fpn.pipe_kwarg_bind(fpn.PN_INPUT)
def v(pni, *dtype_specs):
    pni['v'] = dict(dtype_specs=dtype_specs)
    if pni.complete():
        return pni.build()


class Shape(fpn.PipeNodeInput):
    def __init__(self, shape: ShapeType):
        self.shape = shape
        self._ref = dict()

    def __setitem__(self, key, value):
        if key in self._ref:
            raise KeyError('duplicate key', key)
        self._ref[key] = value

    def __repr__(self) -> str:
        return repr(self._ref)

    def complete(self) -> bool:
        return all(k in self._ref for k in tuple('ficv'))

    def build(self) -> sf.Frame:
        count_row, count_col = self.shape
        index = Builder.build_index(count=count_row, **self._ref['i'])
        columns = Builder.build_index(count=count_col, **self._ref['c'])
        blocks = Builder.build_values(shape=self.shape, **self._ref['v'])
        return Builder.build_frame(index=index,
                columns=columns,
                blocks=blocks,
                **self._ref['f'],
                )