import numpy as np

import static_frame as sf

import frame_fixtures as ff


# pytest -s --color no --disable-pytest-warnings --tb=native



def test_fixture_factory() -> None:

    msg = 'f(Fg)|i(I,str)|c(IDg,dtD)|v(float)|s(10,10)'
    f1 = ff.Fixture.to_frame(msg)
    assert f1.shape == (10, 10)

    msg = 'f(F)|i((I,I),(str,str))|c((IN,I),(dtns,int))|v(str,bool,object)|s(10,10)'
    f2 = ff.Fixture.to_frame(msg)
    assert f2.shape == (10, 10)

