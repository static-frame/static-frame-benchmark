
import numpy
import static_frame as sf

from .fixtures import FixtureFactory


class FrameA:

    factory_input = 'f(F)|i(I,str)|c(I,str)|v(float)'

    def setup(self):
        f = FixtureFactory.from_str(self.factory_input)(10000, 10)
        self.records = (t for t in f.iter_tuple(axis=1))
        self.items = [(c, f[c].values) for c in f.columns]

    def time_from_records(self):
        f = sf.Frame.from_records(self.records)
        assert f.shape == (10000, 10)

    time_from_records.pretty_name = f'from_records-{factory_input}'


    def time_from_items(self):
        f = sf.Frame.from_items(self.items)
        assert f.shape == (10000, 10)

    time_from_items.pretty_name = f'from_items-{factory_input}'


class FrameB:

    factory_input = 'f(F)|i(I,str)|c(I,str)|v(str,float,int,bool)'

    def setup(self):
        f = FixtureFactory.from_str(self.factory_input)(10000, 10)
        self.records = (t for t in f.iter_tuple(axis=1))
        self.items = [(c, f[c].values) for c in f.columns]

    def time_from_records(self):
        f = sf.Frame.from_records(self.records)
        assert f.shape == (10000, 10)

    time_from_records.pretty_name = f'from_records-{factory_input}'


    def time_from_items(self):
        f = sf.Frame.from_items(self.items)
        assert f.shape == (10000, 10)

    time_from_items.pretty_name = f'from_items-{factory_input}'

