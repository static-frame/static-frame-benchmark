
import static_frame as sf
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

class Prototype:

    #---------------------------------------------------------------------------
    def asv_time_sum_0(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=0)

    def asv_time_sum_1(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=1)



def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame)

@apply_prototype(Prototype)
class FrameA:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(float)'
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype)
class FrameB:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(int,int,bool,bool,float,float)'
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
