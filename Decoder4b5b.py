from myhdl import *


class Decoder4b5b(HardwareBlock):
    def __init__(self, signals = None):
        super().__init__(signals)

    def generateSignals(self, *args):
        self.signals = {}

        self.signals['input'] = Signal(intbv(0)[5:])
        self.signals['out'] = Signal(intbv(0)[4:])

        return self.signals

    def generateBlockFromSignals(self, input, out, error):
        assert(len(input) == 5)
        assert(len(out) == 4)

        @always_comb
        def logic():
            if input in decodingTable4b5b:
                out.next = decodingTable4b5b[input][4:]
                error.next = False
            else:
                out.next = 0
                error.next = True

        return logic

    def generateStimulus(self, *args):
        raise NotImplementedError()
