
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from .fixtures import FixtureFactory
from .fixtures import ShapeType

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_B

from .prototype import apply_prototype

class Prototype:




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    records = [t for t in frame.iter_tuple(axis=1)]
    records_dict = [dict(t) for t in frame.iter_series(axis=1)]
    items = [(c, frame[c].values) for c in frame.columns]

    columns_list = [c for i, c in enumerate(frame.columns) if i % 2]
    columns_slice = slice(frame.columns.iloc[len(frame.columns) // 2], None)
    columns_bool = frame.columns.isin(columns_list)

    index_list = [c for i, c in enumerate(frame.index) if i % 2]
    index_slice = slice(frame.index.iloc[len(frame.index) // 2], None)
    index_bool = frame.index.isin(index_list)

    return SimpleNamespace(
            frame=frame,
            records=records,
            records_dict=records_dict,
            items=items,
            columns_list=columns_list,
            columns_slice=columns_slice,
            columns_bool=columns_bool,
            index_list=index_list,
            index_slice=index_slice,
            index_bool=index_bool,
            )

@apply_prototype(Prototype, InterfaceGroup.Method)
class FrameA:

    FIXTURE = FRAME_A
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype, InterfaceGroup.Method)
class FrameB:

    FIXTURE = FRAME_B
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
