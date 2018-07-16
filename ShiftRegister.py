from myhdl import *
from HardwareBlock import *

class ShiftRegister(HardwareBlock):
    def __init__(self):
        super().__init__(clockTime = 1)

    def generateSignals(self, size = 8):
        self.signals = {}

        self.signals['input'] = Signal(bool(0))
        self.signals['clk'] = Signal(bool(0))
        self.signals['dataOut'] = Signal(intbv(0)[size:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, clk, dataOut):

        tmp = dataOut(len(dataOut)-1, 0)

        @always(clk.posedge)
        def logic():
            dataOut.next[len(dataOut):1] = tmp
            dataOut.next[0] = input

        return logic

    @block
    def generateStimulus(self):

        @instance
        def stimulus():
            for testNumber in range(2**8):
                cur = intbv(testNumber)[8:]

                for shiftCount in reversed(range(8)):
                    self.signals['input'].next = cur[shiftCount]
                    yield delay(2)

                assert(self.signals['dataOut'] == testNumber)

        return stimulus
