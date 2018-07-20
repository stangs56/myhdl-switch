from multiprocessing import Process

import ShiftRegister
import CRCGenerator
import Encoder4b5b
import Decoder4b5b

def test(inst):
    inst.simulate()
    inst.generateVHDL()
    inst.generateVerilog()

def main():
    tests = [ShiftRegister.ShiftRegister(),
        # CRCGenerator.CRCGenerator(),
        Encoder4b5b.Encoder4b5b(),
        Decoder4b5b.Decoder4b5b()]

    # Processes need to be created as myhdl only
    # allows 1 simulation per python instance
    for cur in tests:
        p = Process(target=test, args=(cur,))
        p.start()
        p.join()

if __name__ == '__main__':
    main()
