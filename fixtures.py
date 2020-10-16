import typing as tp
import numpy as np
import random
from itertools import chain
from itertools import cycle
from functools import lru_cache
import string

from static_frame.core.util import DtypeSpecifier
from static_frame.core.container import ContainerOperand

import static_frame as sf
import function_pipe as fpn
# from function_pipe import pipe_node
# from function_pipe import pipe_node_factory

DtypeSpecOrSpecs = tp.Union[DtypeSpecifier, tp.Tuple[DtypeSpecifier, ...]]
DTYPE_OBJECT = np.dtype(object)
MAX_SIZE = 1_000_000


class SourceValues:
    _INTEGERS = None
    _CHARS = None

    @staticmethod
    def shuffle(mutable) -> None:
        state = random.getstate()
        random.seed(42)
        random.shuffle(mutable)
        random.setstate(state)

    @classmethod
    def get_ints(cls) -> tp.Sequence[int]:
        '''Return a fixed sequence of unique integers, of size equal to MAX_SIZE.
        '''
        if not cls._INTEGERS:
            values = list(range(MAX_SIZE))
            cls.shuffle(values)
            cls._INTEGERS = values

        return cls._INTEGERS

    @classmethod
    def get_chars(cls) -> tp.Sequence[str]:

        if not cls._CHARS:
            values = []
            from hashlib import blake2b
            for i in cls.get_ints():
                h = blake2b(digest_size=6)
                h.update(str.encode(str(i)))
                values.append(h.hexdigest())
            cls._CHARS = values

        return cls._CHARS



#-------------------------------------------------------------------------------
def dtype_to_element_iter(dtype: np.dtype) -> tp.Iterator[tp.Any]:

    ints = SourceValues.get_ints()
    chars = SourceValues.get_chars()

    if dtype.kind == 'i': # int
        def gen() -> tp.Iterator[tp.Any]:
            for v in ints:
                yield v * (-1 if v % 3 else 1)

    elif dtype.kind == 'u': # int unsigned
        def gen() -> tp.Iterator[tp.Any]:
            yield from chain(ints[-1000:], ints[:-1000])

    elif dtype.kind == 'f': # float
        def gen() -> tp.Iterator[tp.Any]:
            yield np.nan
            for v in ints:
                yield v * (.001 if v % 3 else -.001)

    elif dtype.kind == 'c': # complex
        def gen() -> tp.Iterator[tp.Any]:
            yield complex(np.nan, np.nan)
            for v, i in zip(chain(ints[-10:], ints[:-10]), ints):
                yield complex(v * (-.001 if v % 3 else .001), i * (.001 if i % 4 else -.001))

    elif dtype.kind == 'b': # boolean
        def gen() -> tp.Iterator[bool]:
            yield True
            yield False
            # make first two values unique
            for v in ints:
                yield v % 2 == 0

    elif dtype.kind in ('U', 'S'): # str
        def gen() -> tp.Iterator[str]:
            yield from chars

    elif dtype.kind == 'O': # object
        def gen() -> tp.Iterator[tp.Any]:
            yield None
            yield True
            yield False

            gens = (dtype_to_element_iter(np.dtype(int)),
                    dtype_to_element_iter(np.dtype(float)),
                    dtype_to_element_iter(np.dtype(str)),
                    )

            for i in range(MAX_SIZE):
                for gen in gens:
                    yield next(gen)

    elif dtype.kind == 'M': # datetime64
        def gen() -> tp.Iterator[np.datetime64]:
            for v in ints:
                ofoo = dtype
                yield np.datetime64(v, np.datetime_data(dtype)[0])

    elif dtype.kind == 'm': # timedelta64
        def gen() -> tp.Iterator[np.datetime64]:
            for v in ints:
                yield np.timedelta64(v, np.datetime_data(dtype)[0])

    else:
        raise NotImplementedError(f'no handling for {dtype}')

    return gen()


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
    elif dtype.kind == 'O':
        array = np.empty(shape=count, dtype=dtype) # object
        for i, v in zip(range(len(array)), gen):
            array[i] = v
    else: # string typpes
        array = np.array([next(gen) for _ in range(count)])

    array.flags.writeable = False
    return array

@lru_cache()
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
        return sf.TypeBlocks.from_blocks(gen()).consolidate()


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
    def __init__(self, count_row: int, count_col: int):
        self.shape = (count_row, count_col)
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