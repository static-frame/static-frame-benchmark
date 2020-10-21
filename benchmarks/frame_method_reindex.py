
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

from .fixtures_reference import FRAME_D

class Prototype:
    # for methods that do index manipulation

    def asv_time_pivot_stack(self, ns: SimpleNamespace):
        _ = ns.frame.pivot_stack()

    def asv_time_pivot_unstack(self, ns: SimpleNamespace):
        _ = ns.frame.pivot_unstack()


    def asv_time_reindex(self, ns: SimpleNamespace):
        # this produces a Frame with an Index with tuples
        _ = ns.frame.reindex(ns.index_list, ns.columns_list)


    def asv_time_relabel_flat(self, ns: SimpleNamespace):
        _ = ns.frame.relabel_flat(index=True, columns=True)


    def asv_time_relabel_level_add(self, ns: SimpleNamespace):
        _ = ns.frame.relabel_level_add(index='A', columns='B')

    def asv_time_relabel_level_drop(self, ns: SimpleNamespace):
        _ = ns.frame.relabel_level_drop(index=1, columns=1)



def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)
    columns_list = [c for i, c in enumerate(frame.columns) if i % 2]
    index_list = [c for i, c in enumerate(frame.index) if i % 2]

    return SimpleNamespace(
            frame=frame,
            columns_list=columns_list,
            index_list=index_list,
            )



@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Method)
class FrameD:

    FIXTURE = FRAME_D
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
