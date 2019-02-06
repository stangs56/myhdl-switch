from myhdl import *
from HardwareBlock import *
from Constants import crcPolynomials16bits, crcPolynomials32bits
from copy import copy

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
    def generateShiftStage(self, clk, tmp, x, useXor):
        @always(clk.posedge)
        def withXor():
            tmp[x].next = tmp[x-1].val ^ tmp[-1].val

        @always(clk.posedge)
        def withoutXor():
            tmp[x].next = tmp[x-1].val

        return withXor if useXor else withoutXor

    @block
    def generateBlockFromSignals(self, input, clk, crcValue, go, done, crcType='ethernet'):
        coeffs = crcPolynomials32bits[crcType]

        states = enum('WAIT', 'RUNNING', 'OUTPUT')
        curState = Signal(states.WAIT)

        tmp = [Signal(intbv(1)[1:]) for _ in range(len(crcValue))]
        tmp2 = ConcatSignal(*reversed(tmp))

        stages = []
        print(coeffs)

        for i in range(1, len(tmp)):
            stages.append(self.generateShiftStage(clk, tmp, i, i in coeffs))

        @always(clk.posedge)
        def logic():
            done.next = False
            curState.next = curState.val

            if curState == states.WAIT:
                if go:
                    curState.next = states.RUNNING

            elif curState == states.RUNNING:
                tmp[0].next = input ^ tmp[-1].val

                if not go:
                    curState.next = states.OUTPUT

            elif curState == states.OUTPUT:
                done.next = True
                crcValue.next = tmp2 ^ ((2**len(tmp2)) - 1)

                if not go:
                    curState.next = states.WAIT

                #tmp[0].next = intbv(0)

        return logic, stages

    @block
    def generateStimulus(self):

        # testing values from
        # https://crccalc.com/
        # http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
        tests = [ (int('0x313233343536373839', 16), int('0xCBF43926', 16)) ]

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

                yield delay(6)

                assert(self.signals['done'])
                assert(self.signals['crcValue'] == testCase[1])


        return stimulus
