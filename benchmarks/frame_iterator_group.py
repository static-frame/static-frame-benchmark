
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

from .fixtures_reference import FRAME_E
from .fixtures_reference import FRAME_F

from .prototype import apply_prototype

class Prototype:

    def asv_time_iter_group_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_group(ns.frame.columns.iloc[0]):
            pass

    def asv_time_iter_group_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_group(ns.frame.columns.iloc[0]).apply(lambda f: f.shape)

    def asv_time_iter_group_labels_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_group_labels(-1, axis=0):
            pass

    def asv_time_iter_group_0_labels_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_group_labels(-1, axis=0).apply(lambda f: f.shape)




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Iterator)
class FrameE:

    FIXTURE = FRAME_E
    SHAPE = (100, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Iterator)
class FrameF:

    FIXTURE = FRAME_F
    SHAPE = (100, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
