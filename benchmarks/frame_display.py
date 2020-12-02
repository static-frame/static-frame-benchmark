
from types import SimpleNamespace
import static_frame as sf
from static_frame.core.interface import InterfaceGroup

import frame_fixtures as ff

from .fixtures_reference import FRAME_A
from .fixtures_reference import FRAME_D

from .prototype import apply_prototype

class Prototype:

    def asv_time_display(self, ns: SimpleNamespace):
        _ = ns.frame.display()

    # def asv_time_interface(self, ns: SimpleNamespace):
    #     _ = ns.frame.interface


def create_fixtures(fixture: str):
    frame = ff.parse(fixture)

    return SimpleNamespace(
            frame=frame,
            )

@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Display)
class FrameA:

    FIXTURE = FRAME_A

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)


@apply_prototype(Prototype, sf.Frame, InterfaceGroup.Display)
class FrameD:

    FIXTURE = FRAME_D

    def setup_cache(self) -> SimpleNamespace:
        return create_fixtures(self.FIXTURE)
