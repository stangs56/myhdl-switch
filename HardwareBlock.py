from myhdl import *


class HardwareBlock:
    def __init__(self, signals = None, clockTime = None, simLength = 3000):
        self.signals = signals
        self.clockTime = clockTime
        self.simLength = simLength

    def generateSignals(self, *args):
        raise NotImplementedError()

    def generateBlockFromSignals(self, *args):
        raise NotImplementedError()

    def generateStimulus(self, *args):
        raise NotImplementedError()

    @block
    def createBlock(self):
        if self.signals is None:
            self.signals = self.generateSignals()

        self.inst = self.generateBlockFromSignals(**self.signals)
        return self.inst

    def generateVHDL(self):
        self.createBlock()
        self.inst.convert(hdl='VHDL')

    def gerateVerilog(self):
        self.createBlock()
        self.inst.conver(hdl='Verilog')

    @block
    def testInst(self):
        self.createBlock()
        self.stimulus = self.generateStimulus()

        @always(delay(0 if self.clockTime is None else self.clockTime))
        def clkgen():
            self.signals['clk'].next = not self.signals['clk']

        if self.clockTime is None:
            return self.inst, self.stimulus
        else:
            return self.inst, clkgen, self.stimulus

    def simulate(self):
        test = self.testInst()
        test.config_sim(trace=True)
        test.run_sim(self.simLength)
