from myhdl import *
from HardwareBlock import *
from Constants import crcPolynomials16bits, crcPolynomials32bits

class CRCGenerator(HardwareBlock):
    def generateSignals(self, size=32):
        self.signals = {}

        self.signals['input'] = Signal(bool(0))
        self.signals['clk'] = Signal(bool(0))
        self.signals['crcValue'] = Signal(intbv(0)[size:])

        return self.signals

    @block
    def generateBlockFromSignals(self, input, clk, crcValue, crcType='ethernet'):
        raise NotImplementedError()

    @block
    def generateStimulus(self):
        raise NotImplementedError()
