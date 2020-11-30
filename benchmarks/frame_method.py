
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

from types import SimpleNamespace
import frame_fixtures as ff
from .prototype import apply_prototype

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_C

class Prototype:
    '''Mostly numeric methods; for reindexing and related operations, see frame_method_reindex.py'.
    '''

    def asv_time_any_0(self, ns: SimpleNamespace):
        _ = ns.frame.any(axis=0)

    def asv_time_any_1(self, ns: SimpleNamespace):
        _ = ns.frame.any(axis=1)


    def asv_time_astype_element(self, ns: SimpleNamespace):
        _ = ns.frame.astype(str)

    # might try astype with iterable

    def asv_time_clip(self, ns: SimpleNamespace):
        _ = ns.frame.clip(lower=0, upper=1)



    def asv_time_cumsum_0(self, ns: SimpleNamespace):
        _ = ns.frame.cumsum(axis=0)

    def asv_time_cumsum_1(self, ns: SimpleNamespace):
        _ = ns.frame.cumsum(axis=1)


    def asv_time_drop_duplicated_0(self, ns: SimpleNamespace):
        _ = ns.frame.drop_duplicated(axis=0)

    def asv_time_drop_duplicated_1(self, ns: SimpleNamespace):
        _ = ns.frame.drop_duplicated(axis=1)


    def asv_time_dropna_0(self, ns: SimpleNamespace):
        _ = ns.frame.dropna(axis=0)

    def asv_time_dropna_1(self, ns: SimpleNamespace):
        _ = ns.frame.dropna(axis=1)


    def asv_time_equals(self, ns: SimpleNamespace):
        _ = ns.frame.equals(ns.frame_alt)


    def asv_time_fillna(self, ns: SimpleNamespace):
        _ = ns.frame.fillna(None)


    def asv_time_fillna_leading_0(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_leading(None, axis=0)

    def asv_time_fillna_leading_1(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_leading(None, axis=1)


    def asv_time_fillna_trailing_0(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_trailing(None, axis=0)

    def asv_time_fillna_trailing_1(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_trailing(None, axis=1)


    def asv_time_fillna_forward_0(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_forward(axis=0)

    def asv_time_fillna_forward_1(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_forward(axis=1)


    def asv_time_fillna_backward_0(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_backward(axis=0)

    def asv_time_fillna_backward_1(self, ns: SimpleNamespace):
        _ = ns.frame.fillna_backward(axis=1)


    # getting all-nan slice
    # def asv_time_iloc_max_0(self, ns: SimpleNamespace):
    #     _ = ns.frame.iloc_max(skipna=True, axis=0)

    # def asv_time_iloc_max_1(self, ns: SimpleNamespace):
    #     _ = ns.frame.iloc_max(skipna=True, axis=1)


    def asv_time_isin(self, ns: SimpleNamespace):
        _ = ns.frame.isin((0, 10))

    def asv_time_isna(self, ns: SimpleNamespace):
        _ = ns.frame.isna()


    def asv_time_notna(self, ns: SimpleNamespace):
        _ = ns.frame.notna()


    def asv_time_shift(self, ns: SimpleNamespace):
        _ = ns.frame.shift(10, 10)

    def asv_time_roll(self, ns: SimpleNamespace):
        _ = ns.frame.roll(10, 10)


    def asv_time_sort_columns(self, ns: SimpleNamespace):
        _ = ns.frame.sort_columns()

    def asv_time_sort_index(self, ns: SimpleNamespace):
        _ = ns.frame.sort_index()


    def asv_time_sort_values_0(self, ns: SimpleNamespace):
        _ = ns.frame.sort_values(ns.frame.index.iloc[0], axis=0)

    def asv_time_sort_values_1(self, ns: SimpleNamespace):
        _ = ns.frame.sort_values(ns.frame.columns.iloc[0], axis=1)


    def asv_time_sum_0(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=0)

    def asv_time_sum_1(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=1)


    def asv_time_unique_0(self, ns: SimpleNamespace):
        _ = ns.frame.unique(axis=0)

    def asv_time_unique_1(self, ns: SimpleNamespace):
        _ = ns.frame.unique(axis=1)


def create_fixtures(fixture: str):
    frame = ff.Fixture.to_frame(fixture)
    frame_alt = frame.assign.iloc[0, 0](-1)

    return SimpleNamespace(
            frame=frame,
            frame_alt=frame_alt,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Method)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Method)
class FrameC:

    FIXTURE = FRAME_C

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
