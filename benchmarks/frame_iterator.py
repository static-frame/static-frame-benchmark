
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

import frame_fixtures as ff

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B

from .prototype import apply_prototype

class Prototype:

    # NOTE: apply are given trivial functions, as we are not trying to measure the function application, the creation of the resulting Series

    def asv_time_iter_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(0):
            pass

    def asv_time_iter_array_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_array(0).apply(lambda a: a.dtype)


    def asv_time_iter_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(1):
            pass

    def asv_time_iter_array_1_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_array(1).apply(lambda a: a.dtype)




    def asv_time_iter_tuple_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(0):
            pass

    def asv_time_iter_tuple_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_tuple(0).apply(lambda t: len(t))


    def asv_time_iter_tuple_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(1):
            pass

    def asv_time_iter_tuple_1_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_tuple(1).apply(lambda t: len(t))




    def asv_time_iter_series_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(0):
            pass

    def asv_time_iter_series_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_series(0).apply(lambda s: s.dtype)


    def asv_time_iter_series_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(1):
            pass

    def asv_time_iter_series_1_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_series(1).apply(lambda s: s.dtype)




    def asv_time_iter_window_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=0):
            pass

    def asv_time_iter_window_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_window(size=10, axis=0).apply(lambda w: w.shape)


    def asv_time_iter_window_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=1):
            pass

    def asv_time_iter_window_1_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_window(size=10, axis=1).apply(lambda w: w.shape)




    def asv_time_iter_window_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=0):
            pass

    def asv_time_iter_window_array_0_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_window_array(size=10, axis=0).apply(lambda w: w.shape)


    def asv_time_iter_window_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=1):
            pass

    def asv_time_iter_window_array_1_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_window_array(size=10, axis=1).apply(lambda w: w.shape)




    def asv_time_iter_element(self, ns: SimpleNamespace):
        for part in ns.frame.iter_element():
            pass

    def asv_time_iter_element_apply(self, ns: SimpleNamespace):
        _ = ns.frame.iter_element().apply(str)




def create_fixtures(fixture: str):
    frame = ff.Fixture.to_frame(fixture)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Iterator)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Iterator)
class FrameB:

    FIXTURE = FRAME_B

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
