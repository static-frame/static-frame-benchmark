
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
import frame_fixtures as ff
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_C

class Prototype:

    def asv_time_binary_add_element(self, ns: SimpleNamespace):
        _ = ns.frame + 10

    def asv_time_binary_add_array(self, ns: SimpleNamespace):
        _ = ns.frame + ns.frame.values

    def asv_time_binary_eq_element(self, ns: SimpleNamespace):
        _ = ns.frame == 10

    def asv_time_binary_eq_array(self, ns: SimpleNamespace):
        _ = ns.frame == ns.frame.values




def create_fixtures(fixture: str):
    frame = ff.Fixture.to_frame(fixture)

    return SimpleNamespace(
            frame=frame)

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.OperatorBinary)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.OperatorBinary)
class FrameC:

    FIXTURE = FRAME_C

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
