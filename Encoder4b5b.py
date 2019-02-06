from myhdl import *
from HardwareBlock import *
from Constants import encodingTable4b5b

class Encoder4b5b(HardwareBlock):
    def __init__(self, signals = None):
        super().__init__(signals)

    def generateSignals(self, *args):
        self.signals = {}

        self.signals['input'] = Signal(intbv(0)[4:])
        self.signals['out'] = Signal(intbv(0)[5:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, out):

        assert(len(input) == 4)
        assert(len(out) == 5)

        @always_comb
        def logic():
            out.next = encodingTable4b5b[input.val]

        return logic

    @block
    def generateStimulus(self, *args):

        @instance
        def stimulus():
            for i in range(2**4):
                self.signals['input'].next = i
                yield delay(1)
                assert(self.signals['out'] == encodingTable4b5b[i])

        return stimulus
