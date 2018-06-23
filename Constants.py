from myhdl import *

encodingTable4b5b = ['11110', '01001', '10100', '10101',
                '01010', '01011', '01110', '01111',
                '10010', '10011', '10110', '10111',
                '11010', '11011', '11100', '11101']

encodingTable4b5b = [intbv(tmp) for tmp in encodingTable4b5b]

#decodingTable4b5b = {encodingTable4b5b[i] : intbv(i) for i in range(2**4)}
