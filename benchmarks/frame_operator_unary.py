
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
import frame_fixtures as ff
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_C

class Prototype:

    def asv_time_unary_abs(self, ns: SimpleNamespace):
        _ = abs(ns.frame)



def create_fixtures(fixture: str):
    frame = ff.Fixture.to_frame(fixture)
    return SimpleNamespace(
            frame=frame)

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.OperatorUnary)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.OperatorUnary)
class FrameC:

    FIXTURE = FRAME_C

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
