from myhdl import *


# 4b5b encoding
encodingTable4b5b = ['11110', '01001', '10100', '10101',
                '01010', '01011', '01110', '01111',
                '10010', '10011', '10110', '10111',
                '11010', '11011', '11100', '11101']

decodingTable4b5b = {encodingTable4b5b[i] : intbv(i) for i in range(2**4)}

encodingTable4b5b = tuple([int(tmp, 2) for tmp in encodingTable4b5b])

# crc polynomials
crcPolynomials16bits = {'x25' : (16, 12, 5, 0, ), 'crc-16' : (16, 15, 2, 0,)}

crcPolynomials32bits = {'ethernet' : (32, 26, 23, 22, 16, 12, 11, 10, 8, 7, 5, 4, 2, 1, 0, )}
