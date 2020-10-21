
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B

from .prototype import apply_prototype

class Prototype:


    def asv_time_from_concat_0(self, ns: SimpleNamespace):
        sf.Frame.from_concat((ns.frame, ns.frame, ns.frame),
                axis=0,
                index=sf.IndexAutoFactory)

    def asv_time_from_concat_1(self, ns: SimpleNamespace):
        sf.Frame.from_concat((ns.frame, ns.frame, ns.frame),
                axis=1,
                columns=sf.IndexAutoFactory)

    def asv_time_from_concat_items_0(self, ns: SimpleNamespace):
        sf.Frame.from_concat_items(enumerate((ns.frame, ns.frame, ns.frame)),
                axis=0)

    def asv_time_from_concat_items_1(self, ns: SimpleNamespace):
        sf.Frame.from_concat_items(enumerate((ns.frame, ns.frame, ns.frame)),
                axis=1)

    # from_overlay: need multiple frames

    def asv_time_from_records(self, ns: SimpleNamespace):
        f = sf.Frame.from_records(ns.records)

    def asv_time_from_dict_records(self, ns: SimpleNamespace):
        f = sf.Frame.from_dict_records(ns.records_dict)

    # from_records_items
    # from_dict_records_items

    def asv_time_from_items(self, ns: SimpleNamespace):
        f = sf.Frame.from_items(ns.items)

    # from_dict: same as from_items




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    records = [t for t in frame.iter_tuple(axis=1)]
    records_dict = [dict(t) for t in frame.iter_series(axis=1)]
    items = [(c, frame[c].values) for c in frame.columns]

    return SimpleNamespace(
            frame=frame,
            records=records,
            records_dict=records_dict,
            items=items,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Constructor)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Constructor)
class FrameB:

    FIXTURE = FRAME_B
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
