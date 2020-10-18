
import static_frame as sf
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

class Prototype:

    #---------------------------------------------------------------------------
    # constructors

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

    #---------------------------------------------------------------------------
    # frame attrs, utility methods

    def asv_time_values(self, ns: SimpleNamespace):
        _ = ns.frame.values

    def asv_time_display(self, ns: SimpleNamespace):
        _ = ns.frame.display()

    def asv_time_astype_element(self, ns: SimpleNamespace):
        _ = ns.frame.astype(str)

    # might try astype with iterable

    #---------------------------------------------------------------------------
    # frame selection

    def asv_time_getitem_element(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_list[0]]

    def asv_time_getitem_list(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_list]

    def asv_time_getitem_slice(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_slice]

    def asv_time_getitem_bool(self, ns: SimpleNamespace):
        _ = ns.frame[ns.columns_bool]


    def asv_time_loc_element_0(self, ns: SimpleNamespace):
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



# NOTE: could not get setup_cache to work unless implemented explicitly on the derived class
# see https://github.com/airspeed-velocity/asv/issues/880


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

@apply_prototype(Prototype)
class FrameA:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(float)'
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype)
class FrameB:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(str,float,int,bool)'
    SHAPE = (1000, 10)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
