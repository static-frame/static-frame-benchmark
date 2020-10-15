import numpy as np

import static_frame as sf

from fixtures import dtype_to_element_iter
from fixtures import dtype_to_array
from fixtures import dtype_spec_to_array

from fixtures import Builder


# pytest -s --color no --disable-pytest-warnings --tb=native

def test_dtype_to_element_iter_a() -> None:
    gen = dtype_to_element_iter(np.dtype(int))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [0, -100, 25, -85555555, 23485, 0, -100, 25]


def test_dtype_to_array_a() -> None:
    a1 = dtype_to_array(np.dtype(int), 4)
    assert a1.tolist() == [0, -100, 25, -85555555]

    a2 = dtype_to_array(np.dtype(object), 4)
    assert a2.tolist() == [None, 'foo', 2.5, False]


def test_spec_to_array_a() -> None:

    a1 = dtype_spec_to_array((int, bool, str), 4)
    assert a1.shape == (4,)
    assert a1[0] == (0, False, 'foo')

    # import ipdb; ipdb.set_trace()


#-------------------------------------------------------------------------------

def test_build_index_a() -> None:

    ix1 = Builder.build_index(4, sf.IndexHierarchy, (int, bool))
    ix2 = Builder.build_index(4, (sf.Index, sf.Index), (int, bool))

    assert ix1.shape == (4, 2)
    assert ix1.equals(ix2)

def test_build_index_b() -> None:

    with self.assertRaises(RuntimeError):
        _ = Builder.build_index(4, (sf.Index, sf.IndexGO), (int, bool))

    ix1 = Builder.build_index(4, (sf.IndexGO, sf.IndexGO), (int, bool))

    import ipdb; ipdb.set_trace()


def test_build_index_b() -> None:

    ix1 = Builder.build_index(4, sf.IndexDate, int)
    assert ix1.__class__ == sf.IndexDate



def test_build_values_a() -> None:

    ix1 = Builder.build_values((4, 8), (int, bool, str))

    assert ix1.shapes.tolist() == [(4,), (4,), (4,), (4,), (4,), (4,), (4,), (4,)]




#-------------------------------------------------------------------------------

def test_node_a() -> None:

    from fixtures import f, i, c, v
    from fixtures import dtY, dtM, dtD, dts, dtns
    from fixtures import F, Fg, I, Ig, IDg, Shape


    post = f(Fg)|i(I,str)|c((Ig,IDg),(int,dtD))|v(bool,int,str,(bool,int))

    f1 = post[Shape((2, 2))]
    print(f1)

    # f1 = post[Shape((4, 8))]
    # import ipdb; ipdb.set_trace()


