from myhdl import *
from HardwareBlock import *
from Constants import crcPolynomials16bits, crcPolynomials32bits

class CRCGenerator(HardwareBlock):
    def generateSignals(self, size=32):
        self.signals = {}

        self.signals['input'] = Signal(bool(0))
        self.signals['clk'] = Signal(bool(0))
        self.signals['go'] = Signal(bool(0))
        self.signals['done'] = Signal(bool(0))
        self.signals['crcValue'] = Signal(intbv(0)[size:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, clk, crcValue, go, done, crcType='ethernet'):

        @always(clk.posedge)
        def logic():
            pass

        return logic

    @block
    def generateStimulus(self):

        # testing values from
        # https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/
        tests = [ (int('0x313233343536373839', 16), int('0x04C11DB7', 16)) ]

        @instance
        def stimulus():
            for testCase in tests:
                testBv = intbv(testCase[0])

                self.signals['go'].next = True
                self.signals['input'].next = testBv[0]

                yield delay(2)

                for bitIdx in range(1, len(testBv)):
                    self.signals['input'].next = testBv[bitIdx]
                    yield delay(2)

                assert(self.signals['done'])
                assert(self.signals['crcValue'] == testCase[1])


        return stimulus
