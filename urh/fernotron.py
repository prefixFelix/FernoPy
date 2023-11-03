#!/usr/bin/env python3

import sys


def decode(bits):
    msg = ['']*12
    msg_str = ''

    # Check length
    if not len(bits) == 481:
        if len(bits) < 481:
            raise Exception('Frame to short!')
        else:
            raise Exception('Frame to long!')

    # Check preamble
    if not bits[0:12] == '101010101010':
        raise Exception('Preamble error!')

    # Check / decode data
    p = 12
    for i in range(12):
        # Check gap
        if not bits[p:p+9] == "100000000":
            raise Exception(f'Gap error in front of block {i}!')
        p += 9

        # Check fields and decode bits to symbols
        for j in range(10):
            bit = bits[p:p+3]
            if bit == '110':
                msg[i] += '0'
            elif bit == '100':
                msg[i] += '1'
            else:
                raise Exception(f'Symbol error! Got: {bit} at block {i} and symbol {j}!')
            p += 3

    # Convert bytes into little endian / remove two parity bits
    for i, field in enumerate(msg):
        msg[i] = field[0:8][::-1]

    # Build bit sequence out of fields / ignore double frames
    checksum, last_field = 0, 0
    for i, field in enumerate(msg):
        if i % 2:
            # Calculate checksum
            checksum += int(field, 2)
            last_field = int(field, 2)

            msg_str += field

    # Check checksum
    checksum -= last_field          # Ignore last fields
    checksum = hex(checksum)[-2:]   # Only use leading 2 nibbles
    checksum = int(checksum, 16)

    check_checksum = False
    if check_checksum and checksum != last_field:
        raise Exception(f'Checksum error!')

    # Write to URH
    sys.stdout.write(msg_str)

def encode(bits):
    # TODO
    print('NOT IMPLEMENTED')


def main(argv):

    if argv[1] == 'e':
        encode(argv[2])
    elif argv[1] == 'd':
        decode(argv[2])
    else:
        raise Exception('Please provide a mode via cl-parameter (e or d)!')


if __name__ == '__main__':
    main(sys.argv)
