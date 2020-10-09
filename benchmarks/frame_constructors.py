
import numpy
import static_frame as sf

class FromRecords:

    # params = [None, 1000]
    # param_names = ["nrows"]

    # # Generators get exhausted on use, so run setup before every call
    # number = 1
    # repeat = (3, 250, 10)

    def setup(self):
        N = 100000
        self.gen = ((x, x * 20, x * 100) for x in range(N))

    def time_frame_from_records(self):
        f = sf.Frame.from_records(self.gen)


