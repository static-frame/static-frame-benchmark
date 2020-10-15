import numpy as np

from fixtures import dtype_to_element
from fixtures import dtype_to_array



# pytest -s --color no --disable-pytest-warnings --tb=native

def test_dtype_to_element_a():
    gen = dtype_to_element(np.dtype(int))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [0, -100, 25, -85555555, 23485, 0, -100, 25]


def test_dtype_to_array_a():
    a1 = dtype_to_array(np.dtype(int), 4)
    assert a1.tolist() == [0, -100, 25, -85555555]

    a2 = dtype_to_array(np.dtype(object), 4)
    assert a2.tolist() == [None, 'foo', 2.5, False]


    # import ipdb; ipdb.set_trace()


def test_node_a():

    from fixtures import f, i, c, v
    from fixtures import F, I, Shape

    post = f(F)|i(I,str)|c(I,int)|v(bool,int)

    shape = Shape((4, 8))
    post[shape]
    print(shape)

    # import ipdb; ipdb.set_trace()