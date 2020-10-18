
import static_frame as sf
from types import SimpleNamespace
from .fixtures import FixtureFactory
from .fixtures import ShapeType
from .prototype import apply_prototype

class Prototype:

    #---------------------------------------------------------------------------
    # arithmetic methods

    def asv_time_sum_0(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=0)

    def asv_time_sum_1(self, ns: SimpleNamespace):
        _ = ns.frame.sum(axis=1)

    def asv_time_cumsum_0(self, ns: SimpleNamespace):
        _ = ns.frame.cumsum(axis=0)

    def asv_time_cumsum_1(self, ns: SimpleNamespace):
        _ = ns.frame.cumsum(axis=1)

    def asv_time_any_0(self, ns: SimpleNamespace):
        _ = ns.frame.any(axis=0)

    def asv_time_any_1(self, ns: SimpleNamespace):
        _ = ns.frame.any(axis=1)


    #---------------------------------------------------------------------------
    # nan methods

    def asv_time_isna(self, ns: SimpleNamespace):
        _ = ns.frame.isna()

    def asv_time_notna(self, ns: SimpleNamespace):
        _ = ns.frame.notna()


    def asv_time_dropna_0(self, ns: SimpleNamespace):
        _ = ns.frame.dropna(axis=0)

    def asv_time_dropna_1(self, ns: SimpleNamespace):
        _ = ns.frame.dropna(axis=1)


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

    #---------------------------------------------------------------------------
    # unary, binary operators

    def asv_time_unary_abs(self, ns: SimpleNamespace):
        _ = abs(ns.frame)

    def asv_time_binary_add_element(self, ns: SimpleNamespace):
        _ = ns.frame + 10

    def asv_time_binary_add_array(self, ns: SimpleNamespace):
        _ = ns.frame + ns.frame.values

    def asv_time_binary_eq_element(self, ns: SimpleNamespace):
        _ = ns.frame == 10

    def asv_time_binary_eq_array(self, ns: SimpleNamespace):
        _ = ns.frame == ns.frame.values




def create_fixtures(fixture: str, shape: ShapeType):
    frame = FixtureFactory.from_str(fixture)(shape)

    return SimpleNamespace(
            frame=frame)

@apply_prototype(Prototype)
class FrameA:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(float)'
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)


@apply_prototype(Prototype)
class FrameB:

    FIXTURE = 'f(F)|i(I,str)|c(I,str)|v(int,int,bool,float,float,float)'
    SHAPE = (1000, 100)

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE, self.SHAPE)
