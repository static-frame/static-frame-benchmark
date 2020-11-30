
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup
import frame_fixtures as ff

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B

from .prototype import apply_prototype

class Prototype:


    def asv_time_values(self, ns: SimpleNamespace):
        _ = ns.frame.values

    def asv_time_transpose(self, ns: SimpleNamespace):
        _ = ns.frame.T

    def asv_time_dtypes(self, ns: SimpleNamespace):
        _ = ns.frame.dtypes


def create_fixtures(fixture: str):
    frame = ff.Fixture.to_frame(fixture)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Attribute)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Attribute)
class FrameB:

    FIXTURE = FRAME_B

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
