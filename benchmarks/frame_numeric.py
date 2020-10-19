
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_C

class Prototype:




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame)

@apply_prototype(Prototype, InterfaceGroup.Method)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, InterfaceGroup.Method)
class FrameC:

    FIXTURE = FRAME_C
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
