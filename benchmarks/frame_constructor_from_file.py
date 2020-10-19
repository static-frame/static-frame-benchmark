
import static_frame as sf
from static_frame.core.interface import InterfaceGroup
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_D

class Prototype:

    #---------------------------------------------------------------------------
    # arithmetic methods

    # from_json?

    def asv_time_from_delimited(self, ns: SimpleNamespace):
        _ = sf.Frame.from_delimited('frame.txt',
                delimiter='|',
                index_depth=ns.frame.index.depth,
                columns_depth=ns.frame.columns.depth,
                )

    def asv_time_from_xlsx(self, ns: SimpleNamespace):
        _ = sf.Frame.from_xlsx('frame.xlsx',
                index_depth=ns.frame.index.depth,
                columns_depth=ns.frame.columns.depth,
                )



#-------------------------------------------------------------------------------
def create_fixtures(fixture: str, shape: ShapeType):
    frame: sf.Frame = FixtureFactory.from_str(fixture)(shape)

    frame.to_delimited('frame.txt',
            delimiter='|',
            include_index=True,
            include_columns=True,)

    frame.to_xlsx('frame.xlsx',
            include_index=True,
            include_columns=True,)

    # return the Frame so we can get the expected index/columns depth
    return SimpleNamespace(
            frame=frame)



@apply_prototype(Prototype, InterfaceGroup.Constructor)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, InterfaceGroup.Constructor)
class FrameD:

    FIXTURE = FRAME_D
    SHAPE = (100, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)