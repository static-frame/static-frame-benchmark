
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

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


def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, InterfaceGroup.Attribute)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, InterfaceGroup.Attribute)
class FrameB:

    FIXTURE = FRAME_B
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
