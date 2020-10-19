
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B

from .prototype import apply_prototype

class Prototype:

    #---------------------------------------------------------------------------
    # basic iteration

    def asv_time_iter_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(0):
            pass

    def asv_time_iter_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(1):
            pass


    def asv_time_iter_tuple_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(0):
            pass

    def asv_time_iter_tuple_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(1):
            pass

    def asv_time_iter_series_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(0):
            pass

    def asv_time_iter_series_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(1):
            pass

    # NOTE: need to have a boolean column to use for grouping
    # iter_group
    # iter_group_labels

    def asv_time_iter_window_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=0):
            pass

    def asv_time_iter_window_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=1):
            pass


    def asv_time_iter_window_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=0):
            pass

    def asv_time_iter_window_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=1):
            pass

    def asv_time_iter_element(self, ns: SimpleNamespace):
        for part in ns.frame.iter_element():
            pass




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, InterfaceGroup.Iterator)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, InterfaceGroup.Iterator)
class FrameB:

    FIXTURE = FRAME_B
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
