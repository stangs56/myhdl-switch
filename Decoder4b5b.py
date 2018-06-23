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
        self.signals['error'] = Signal(intbv(0)[1:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, out, error):
        assert(len(input) == 5)
        assert(len(out) == 4)

        @always_comb
        def logic():
            if int(input) in decodingTable4b5b:
                out.next = decodingTable4b5b[int(input)][4:]
                error.next = False
            else:
                out.next = 0
                error.next = True

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
                    assert(self.signals['error'] == False)
                else:
                    assert(self.signals['out'] == 0)
                    assert(self.signals['error'] == True)

        return stimulus
