
import numpy
import static_frame as sf
from hashlib import blake2b
import pickle
import os

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

# @classmethod
# def get_cache_name(cls) -> str:
#     h = blake2b(digest_size=6)
#     h.update(str.encode(cls.FACTORY_INPUT + str(cls.SHAPE)))
#     return h.hexdigest()

# def setup_cache(self):
#     frame = FixtureFactory.from_str(self.FACTORY_INPUT)(self.SHAPE)
#     print(os.getcwd())
#     with open(self.get_cache_name(), 'wb') as f:
#         pickle.dump(frame, f)

@set_methods_name
class FrameA:

    FACTORY_INPUT = 'f(F)|i(I,str)|c(I,str)|v(float)'
    SHAPE = (1000, 10)


    def setup(self):

        frame = FixtureFactory.from_str(self.FACTORY_INPUT)(self.SHAPE)

        self.records = [t for t in frame.iter_tuple(axis=1)]
        self.records_dict = [dict(t) for t in frame.iter_series(axis=1)]

        self.items = [(c, frame[c].values) for c in frame.columns]
        self.frame = frame
        # self.series = frame[frame.columns[0]]

    #---------------------------------------------------------------------------
    def time_from_concat_0(self):
        sf.Frame.from_concat((self.frame, self.frame, self.frame),
                axis=0,
                index=sf.IndexAutoFactory)

    def time_from_concat_1(self):
        sf.Frame.from_concat((self.frame, self.frame, self.frame),
                axis=1,
                columns=sf.IndexAutoFactory)

    def time_from_concat_items_0(self):
        sf.Frame.from_concat_items(enumerate((self.frame, self.frame, self.frame)),
                axis=0)

    def time_from_concat_items_1(self):
        sf.Frame.from_concat_items(enumerate((self.frame, self.frame, self.frame)),
                axis=1)

    # from_overlay: need multiple frames

    def time_from_records(self):
        f = sf.Frame.from_records(self.records)
        assert f.shape == self.SHAPE

    def time_from_dict_records(self):
        f = sf.Frame.from_dict_records(self.records_dict)
        assert f.shape == self.SHAPE

    # from_records_items
    # from_dict_records_items

    def time_from_items(self):
        f = sf.Frame.from_items(self.items)
        assert f.shape == self.SHAPE

    # from_dict: same as from_items

    #---------------------------------------------------------------------------

    def time_iter_array_0(self):
        for part in self.frame.iter_array(0):
            pass

    def time_iter_array_1(self):
        for part in self.frame.iter_array(1):
            pass


    def time_iter_tuple_0(self):
        for part in self.frame.iter_tuple(0):
            pass

    def time_iter_tuple_1(self):
        for part in self.frame.iter_tuple(1):
            pass

    def time_iter_series_0(self):
        for part in self.frame.iter_series(0):
            pass

    def time_iter_series_1(self):
        for part in self.frame.iter_series(1):
            pass

    # NOTE: need to have a boolean column to use for grouping
    # iter_group
    # iter_group_labels

    def time_iter_window_0(self):
        for part in self.frame.iter_window(size=10, axis=0):
            pass

    def time_iter_window_1(self):
        for part in self.frame.iter_window(size=10, axis=1):
            pass


    def time_iter_window_array_0(self):
        for part in self.frame.iter_window_array(size=10, axis=0):
            pass

    def time_iter_window_array_1(self):
        for part in self.frame.iter_window_array(size=10, axis=1):
            pass

    def time_iter_element(self):
        for part in self.frame.iter_element():
            pass

@set_methods_name
class FrameB(FrameA):

    FACTORY_INPUT = 'f(F)|i(I,str)|c(I,str)|v(str,float,int,bool)'
