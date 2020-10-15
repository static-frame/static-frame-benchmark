import numpy as np
from fixtures import dtype_spec_to_element

# pytest -s --color no --disable-pytest-warnings --tb=native

def test_dtype_to_element_a():
    gen = dtype_spec_to_element(np.dtype(int))
    post = [v for _, v in zip(range(8), gen)]
    assert post == [0, -100, 25, -85555555, 23485, 0, -100, 25]