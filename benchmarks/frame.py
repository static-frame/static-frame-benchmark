
import numpy
import static_frame as sf
from hashlib import blake2b
import pickle
import os
from types import SimpleNamespace
from .fixtures import FixtureFactory


def set_methods_name(cls):

    for name in dir(cls):
        if name.startswith('time_'):
            func = getattr(cls, name)
            name = f"{name.replace('time_', '')}-{cls.FACTORY_INPUT}"
            print(cls, name)
            func.pretty_name = name
    return cls

# NOTE: could not get setup_cache to work unless implemented explicitly on the derived class; not sure how to get reuse from method; tried assigning in decorator

@set_methods_name
class FrameA:

    FACTORY_INPUT = 'f(F)|i(I,str)|c(I,str)|v(float)'
    SHAPE = (1000, 10)

    @classmethod
    def get_cache_name(cls) -> str:
        h = blake2b(digest_size=6)
        h.update(str.encode(cls.FACTORY_INPUT + str(cls.SHAPE)))
        return h.hexdigest()

    @classmethod
    def create_fixtures(cls):
        frame = FixtureFactory.from_str(cls.FACTORY_INPUT)(cls.SHAPE)

        records = [t for t in frame.iter_tuple(axis=1)]
        records_dict = [dict(t) for t in frame.iter_series(axis=1)]
        items = [(c, frame[c].values) for c in frame.columns]

        return SimpleNamespace(records=records,
                records_dict=records_dict,
                items=items,
                frame=frame)

    def setup_cache(self) -> SimpleNamespace:
        return self.create_fixtures()

    #---------------------------------------------------------------------------
    def time_from_concat_0(self, ns: SimpleNamespace):
        sf.Frame.from_concat((ns.frame, ns.frame, ns.frame),
                axis=0,
                index=sf.IndexAutoFactory)

    def time_from_concat_1(self, ns: SimpleNamespace):
        sf.Frame.from_concat((ns.frame, ns.frame, ns.frame),
                axis=1,
                columns=sf.IndexAutoFactory)

    def time_from_concat_items_0(self, ns: SimpleNamespace):
        sf.Frame.from_concat_items(enumerate((ns.frame, ns.frame, ns.frame)),
                axis=0)

    def time_from_concat_items_1(self, ns: SimpleNamespace):
        sf.Frame.from_concat_items(enumerate((ns.frame, ns.frame, ns.frame)),
                axis=1)

    # from_overlay: need multiple frames

    def time_from_records(self, ns: SimpleNamespace):
        f = sf.Frame.from_records(ns.records)

    def time_from_dict_records(self, ns: SimpleNamespace):
        f = sf.Frame.from_dict_records(ns.records_dict)

    # from_records_items
    # from_dict_records_items

    def time_from_items(self, ns: SimpleNamespace):
        f = sf.Frame.from_items(ns.items)

    # from_dict: same as from_items

    #---------------------------------------------------------------------------

    def time_iter_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(0):
            pass

    def time_iter_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_array(1):
            pass


    def time_iter_tuple_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(0):
            pass

    def time_iter_tuple_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_tuple(1):
            pass

    def time_iter_series_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(0):
            pass

    def time_iter_series_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_series(1):
            pass

    # NOTE: need to have a boolean column to use for grouping
    # iter_group
    # iter_group_labels

    def time_iter_window_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=0):
            pass

    def time_iter_window_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window(size=10, axis=1):
            pass


    def time_iter_window_array_0(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=0):
            pass

    def time_iter_window_array_1(self, ns: SimpleNamespace):
        for part in ns.frame.iter_window_array(size=10, axis=1):
            pass

    def time_iter_element(self, ns: SimpleNamespace):
        for part in ns.frame.iter_element():
            pass

@set_methods_name
class FrameB(FrameA):

    FACTORY_INPUT = 'f(F)|i(I,str)|c(I,str)|v(str,float,int,bool)'

    def setup_cache(self) -> SimpleNamespace:
        return self.create_fixtures()