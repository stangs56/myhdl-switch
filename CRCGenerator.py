from myhdl import *
from HardwareBlock import *
from Constants import crcPolynomials16bits, crcPolynomials32bits

class CRCGenerator(HardwareBlock):
    def __init__(self):
        super().__init__(clockTime = 1)

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
        coeffs = crcPolynomials32bits[crcType]

        states = enum('WAIT', 'RUNNING', 'OUTPUT')
        curState = Signal(states.WAIT)

        tmp = Signal(intbv(0)[len(crcValue):])

        @always(clk.posedge)
        def logic():
            done.next = False

            if curState == states.WAIT:
                if go:
                    curState.next = states.RUNNING
                else:
                    curState.next = states.WAIT
            elif curState == states.RUNNING:
                tmp.next[0] = input ^ tmp[len(tmp)-1]

                for i in range(1, len(tmp)):
                    tmp.next[i] = tmp[i-1] ^ (tmp[len(tmp)-1] if (i in coeffs) else intbv(1)[1:])

                if go:
                    curState.next = states.RUNNING
                else:
                    curState.next = states.OUTPUT
            elif curState == states.OUTPUT:
                done.next = True
                curState.next = states.WAIT
                crcValue.next = tmp
                tmp.next = intbv(0)

        return logic

    @block
    def generateStimulus(self):

        # testing values from
        # https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/
        tests = [ (int('0x313233343536373839', 16), int('0x04C11DB7', 16)) ]

        @instance
        def stimulus():
            self.signals['go'].next = False
            yield delay(4)

            for testCase in tests:
                testBv = intbv(testCase[0])[testCase[0].bit_length():]

                print(testCase[0].bit_length())

                self.signals['go'].next = True

                yield delay(2)

                for bitIdx in range(testCase[0].bit_length()):
                    # assert(not self.signals['done'])
                    print(bitIdx)

                    self.signals['input'].next = testBv[bitIdx]
                    yield delay(2)

                self.signals['go'].next = False

                yield delay(4)

                assert(self.signals['done'])
                assert(self.signals['crcValue'] == testCase[1])


        return stimulus
