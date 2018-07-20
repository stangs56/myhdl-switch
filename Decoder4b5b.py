from myhdl import *
from HardwareBlock import *
from Constants import *

class Decoder4b5b(HardwareBlock):
    def __init__(self, signals = None):
        super().__init__(signals)

    def generateSignals(self, *args):
        self.signals = {}

        self.signals['input'] = Signal(intbv(0)[5:])
        self.signals['out'] = Signal(intbv(0)[4:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, out):
        assert(len(input) == 5)
        assert(len(out) == 4)

        @always_comb
        def logic():
            out.next = decodingTable4b5b[input.val]

        return logic

    @block
    def generateStimulus(self, *args):

        @instance
        def stimulus():
            for i in range(2**5):
                self.signals['input'].next = i
                yield delay(1)
                if i in decodingTable4b5b:
                    assert(self.signals['out'] == decodingTable4b5b[i])
                else:
                    assert(self.signals['out'] == 0)

        return stimulus
