
import static_frame as sf
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

class Prototype:

    #---------------------------------------------------------------------------
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



# NOTE: could not get setup_cache to work unless implemented explicitly on the derived class
# see https://github.com/airspeed-velocity/asv/issues/880


def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    records = [t for t in frame.iter_tuple(axis=1)]
    records_dict = [dict(t) for t in frame.iter_series(axis=1)]
    items = [(c, frame[c].values) for c in frame.columns]

    return SimpleNamespace(records=records,
            records_dict=records_dict,
            items=items,
            frame=frame)

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
