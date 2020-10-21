
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B
from .fixtures_reference import FRAME_D

from .prototype import apply_prototype

class Prototype:

    def asv_time_drop_getitem(self, ns: SimpleNamespace):
        _ = ns.frame.drop[ns.columns_list]

    def asv_time_drop_loc(self, ns: SimpleNamespace):
        _ = ns.frame.drop.loc[ns.index_list, ns.columns_list]


    def asv_time_getitem_element(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_list[0]]

    def asv_time_getitem_list(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_list]

    def asv_time_getitem_slice(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_slice]

    def asv_time_getitem_bool(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_bool]


    def asv_time_loc_element_0(self, ns: SimpleNamespace):
        if ns.frame.index.depth > 1:
            _ = ns.frame.loc[sf.HLoc[ns.index_list[0]]]
        else:
            _ = ns.frame.loc[ns.index_list[0]]


    def asv_time_loc_list_0(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_list]

    def asv_time_loc_slice_0(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_slice]

    def asv_time_loc_bool_0(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_bool]


    def asv_time_loc_element_1(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_list[0], ns.columns_list[0]]

    def asv_time_loc_list_1(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_list, ns.columns_list]

    def asv_time_loc_slice_1(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_slice, ns.columns_slice]

    def asv_time_loc_bool_1(self, ns: SimpleNamespace):
        _ = ns.frame.loc[ns.index_bool, ns.columns_bool]

    # frame.bloc





def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    columns_list = [c for i, c in enumerate(frame.columns) if i % 2]
    columns_slice = slice(frame.columns.iloc[len(frame.columns) // 2], None)
    columns_bool = frame.columns.isin(columns_list)

    index_list = [c for i, c in enumerate(frame.index) if i % 2]
    index_slice = slice(frame.index.iloc[len(frame.index) // 2], None)
    index_bool = frame.index.isin(index_list)

    return SimpleNamespace(
            frame=frame,
            columns_list=columns_list,
            columns_slice=columns_slice,
            columns_bool=columns_bool,
            index_list=index_list,
            index_slice=index_slice,
            index_bool=index_bool,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Selector)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Selector)
class FrameB:

    FIXTURE = FRAME_B
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Selector)
class FrameD:

    FIXTURE = FRAME_D
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
