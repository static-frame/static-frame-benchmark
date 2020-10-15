import numpy as np
from fixtures import dtype_spec_to_element
from fixtures import dtype_to_array

# pytest -s --color no --disable-pytest-warnings --tb=native

def test_dtype_to_element_a():
    gen = dtype_spec_to_element(np.dtype(int))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [0, -100, 25, -85555555, 23485, 0, -100, 25]


def test_dtype_to_array_a():
    a1 = dtype_to_array(np.dytpe(str), 4)
    import ipdb; ipdb.set_trace()
