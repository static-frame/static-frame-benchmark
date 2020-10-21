import numpy as np

import static_frame as sf

from benchmarks.fixtures import dtype_to_element_iter
from benchmarks.fixtures import dtype_to_array
from benchmarks.fixtures import dtype_spec_to_array

from benchmarks.fixtures import Builder
from benchmarks.fixtures import FixtureFactory


# pytest -s --color no --disable-pytest-warnings --tb=native

def test_dtype_to_element_iter_a() -> None:
    gen = dtype_to_element_iter(np.dtype(int))
    post = [v for _, v in zip(range(4), gen)]
    assert post == [-845545, -563150, 468891, 856611]

def test_dtype_to_element_iter_b() -> None:
    gen = dtype_to_element_iter(np.dtype(np.uint8))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [235113, 366960, 998160, 54615, 565621, 785408, 20324, 493152]

def test_dtype_to_element_iter_c() -> None:
    gen = dtype_to_element_iter(np.dtype(complex))
    post = [v for _, v in zip(range(8), gen)]
    # skip the NaN in the first position
    assert post[1:] == [(-107.473+845.5450000000001j), (-772.246+563.15j), (146.316+468.891j), (-234.053+856.611j), (-256.787+597.61j), (-288.389-190.184j), (-777.572+488.334j)]


def test_dtype_to_element_iter_d() -> None:
    gen = dtype_to_element_iter(np.dtype(float))
    post = [v for _, v in zip(range(8), gen)]
    # skip leading NaN
    assert post[1:] == [845.5450000000001, 563.15, -468.891, -856.611, 597.61, 190.184, -488.334]

def test_dtype_to_element_iter_e() -> None:
    gen = dtype_to_element_iter(np.dtype(bool))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [True, False, False, True, False, False, True, True]

def test_dtype_to_element_iter_f() -> None:
    gen = dtype_to_element_iter(np.dtype(str))
    post = [v for _, v in zip(range(4), gen)]
    assert post == ['f1735ae1b619', 'd62d169fd7f9', '2297c5b5755a', 'a75e87c4c1ab']

def test_dtype_to_element_iter_g() -> None:
    gen = dtype_to_element_iter(np.dtype(object))
    post = [v for _, v in zip(range(8), gen)]
    assert post[:4] == [None, True, False, -845545,]
    assert post[5:] == ['f1735ae1b619', -563150, 845.5450000000001]

def test_dtype_to_element_iter_h() -> None:
    gen = dtype_to_element_iter(np.dtype('datetime64[D]'))
    post = [v for _, v in zip(range(4), gen)]
    assert post == [np.datetime64('4285-01-09'), np.datetime64('3511-11-09'), np.datetime64('3253-10-12'), np.datetime64('4315-04-29')]




def test_dtype_to_array_a() -> None:
    a1 = dtype_to_array(np.dtype(int), 4)
    assert a1.tolist() == [-845545, -563150, 468891, 856611]

    a2 = dtype_to_array(np.dtype(object), 4)
    assert a2.tolist() == [None, True, False, -845545]


def test_spec_to_array_a() -> None:

    a1 = dtype_spec_to_array((int, bool, str), 4)
    assert a1.shape == (4,)
    assert a1[0] == (-845545, True, 'f1735ae1b619')



#-------------------------------------------------------------------------------

def test_build_index_a() -> None:

    ix1 = Builder.build_index(4, sf.IndexHierarchy, (int, bool))
    ix2 = Builder.build_index(4, (sf.Index, sf.Index), (int, bool))

    assert ix1.shape == (4, 2)
    assert ix1.equals(ix2)

def test_build_index_b() -> None:

        # _ = Builder.build_index(4, (sf.Index, sf.IndexGO), (int, bool))

    ix1 = Builder.build_index(4, (sf.IndexGO, sf.IndexGO), (int, bool))


def test_build_index_b() -> None:

    ix1 = Builder.build_index(4, sf.IndexDate, int)
    assert ix1.__class__ == sf.IndexDate



def test_build_values_a() -> None:

    ix1 = Builder.build_values((4, 8), (int, bool, str))
    assert ix1.shapes.tolist() == [(4,), (4,), (4,), (4,), (4,), (4,), (4,), (4,)]




# #-------------------------------------------------------------------------------

def test_node_a() -> None:

    from benchmarks.fixtures import f, i, c, v
    from benchmarks.fixtures import dtY, dtM, dtD, dts, dtns
    from benchmarks.fixtures import F, Fg, I, Ig, IDg, Shape


    post = f(Fg)|i(I,str)|c((Ig,IDg),(int,dtD))|v(bool,int,str,(bool,int))

    f1 = post[Shape((2, 2))]
    print(f1)

    assert post[Shape((2000, 6))].shape == (2000, 6)


def test_fixture_factory() -> None:

    msg = 'f(Fg)|i(I,str)|c(IDg,dtD)|v(float)'
    func = FixtureFactory.from_str(msg)

    f1 = func((2, 2))

    msg = 'f(F)|i((I,I),(str,bool))|c((IN,I),(dtns,int))|v(str,bool,object)'
    func = FixtureFactory.from_str(msg)

