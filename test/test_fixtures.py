import pickle

import numpy as np

import static_frame as sf

import frame_fixtures as ff

from benchmarks import fixtures_reference

# pytest -s --color no --disable-pytest-warnings --tb=native

def test_fixtures_a() -> None:
    msg = 'f(Fg)|i(I,str)|c(IDg,dtD)|v(float)|s(10,10)'
    f1 = ff.Fixture.to_frame(msg)
    assert f1.shape == (10, 10)

    msg = 'f(F)|i((I,I),(str,str))|c((IN,I),(dtns,int))|v(str,bool,object)|s(10,10)'
    f2 = ff.Fixture.to_frame(msg)
    assert f2.shape == (10, 10)


def test_fixtures_b() -> None:
    for attr in dir(fixtures_reference):
        if attr.startswith('__'):
            continue
        f = ff.Fixture.to_frame(getattr(fixtures_reference, attr))
        assert isinstance(f, sf.Frame)
