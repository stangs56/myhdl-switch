from multiprocessing import Process
import argparse
from pathlib import Path

import ShiftRegister
import CRCGenerator
import Encoder4b5b
import Decoder4b5b

def test(inst):
    inst.simulate()
    inst.generateVHDL()
    inst.generateVerilog()

def test_all():
    tests = [ShiftRegister.ShiftRegister(),
        # CRCGenerator.CRCGenerator(),
        Encoder4b5b.Encoder4b5b(),
        Decoder4b5b.Decoder4b5b()]

    # Processes need to be created as myhdl only
    # allows 1 simulation per python instance
    for cur in tests:
        print(f'\nTesting: {cur}\n')
        p = Process(target=test, args=(cur,))
        p.start()
        p.join()

def main():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--clean-dir', action='store_true')

    args = parser.parse_args()

    if args.clean_dir:
        #gets full current working directory
        cur = Path().resolve()

        extensions = ['*.v', '*.vhd', '*.vcd']

        for ext in extensions:
            files = cur.rglob(ext)
            for file in files:
                file.unlink()
    else:
        test_all()


if __name__ == '__main__':
    main()
