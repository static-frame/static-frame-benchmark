import os

import static_frame as sf
from static_frame.core.interface import InterfaceGroup
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_C

class Prototype:

    def asv_time_to_delimited(self, ns: SimpleNamespace):
        ns.frame.to_delimited('frame.txt',
                delimiter='|',
                include_index=True,
                include_columns=True,)

    def asv_time_to_xlsx(self, ns: SimpleNamespace):
        ns.frame.to_xlsx('frame.xlsx',
                include_index=True,
                include_columns=True,)

    def asv_time_to_parquet(self, ns: SimpleNamespace):
        ns.frame.to_parquet('frame.parquet',
                include_index=True,
                include_columns=True,)

    def asv_time_to_sqlite(self, ns: SimpleNamespace):
        fn = 'frame.sqlite'
        ns.frame.to_sqlite(fn,
                label='frame',
                include_index=True,
                include_columns=True,)
        # NOTE: cannot do this in setup()
        os.remove(fn)

    def asv_time_to_hdf5(self, ns: SimpleNamespace):
        ns.frame.to_hdf5('frame.hdf5',
                label='frame',
                include_index=True,
                include_columns=True,)


    def asv_time_to_frame_go(self, ns: SimpleNamespace):
        _ = ns.frame.to_frame_go()

    def asv_time_to_html(self, ns: SimpleNamespace):
        _ = ns.frame.to_html()

#-------------------------------------------------------------------------------
def create_fixtures(fixture: str, shape: ShapeType):
    frame: sf.Frame = FixtureFactory.from_str(fixture)(shape)
    return SimpleNamespace(
            frame=frame)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Exporter)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Exporter)
class FrameC:

    FIXTURE = FRAME_C
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
