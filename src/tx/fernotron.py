import gc
import time
import tx_config

def rev(s):
    r = ""
    for c in s:
        r = c + r
    return r

def send_msg(msg_bit, repeat, tx):
    symbol_length = tx_config.general['symbol_length']

    gc.collect()
    for _ in range(repeat):
        # Preambel
        for _ in range(12):
            tx.value(1)
            time.sleep_us(symbol_length)
            tx.value(0)
            time.sleep_us(symbol_length)

        # Data
        for bit in msg_bit:
            if bit == '0':
                # 110
                tx.value(1)
                time.sleep_us(symbol_length * 2)
                tx.value(0)
                time.sleep_us(symbol_length)
            elif bit == '1':
                # 100
                tx.value(1)
                time.sleep_us(symbol_length)
                tx.value(0)
                time.sleep_us(symbol_length * 2)
            else:
                tx.value(1)
                time.sleep_us(symbol_length)
                tx.value(0)
                time.sleep_us(symbol_length * 8)
        tx.value(0)
        time.sleep_us(symbol_length * 100)


def convert_to_bits(msg_hex):
    msg = str(hex(msg_hex))[2:]

    msg_bit = ''
    for i in range(0, len(msg), 2):
        field = msg[i:i + 2]
        field_dec = int(field, 16)
        field_bit = str(bin(field_dec))[2:]

        field_len = len(field_bit)
        if field_len != 8:
            zero_num = 8 - field_len
            field_bit = '0'*zero_num + field_bit

        count_ones = field_bit.count('1')
        if count_ones % 2 == 0:
            parity = ('00', '11')
        else:
            parity = ('01', '10')
        field_reversed = rev(field_bit)

        for j in range(2):
            # Add gap
            msg_bit += 'G'

            suffix = parity[0]
            if j % 2 != 0:
                suffix = parity[1]
            msg_bit += field_reversed + suffix

    return msg_bit + 'G'

# todo COUNTER FIX, MUST CHANGE FOR EACH MSG
def build_msg(device_type, device_id, counter, member, group, cmd):
    print('[!] T:', hex(device_type), 'I:', hex(device_id), 'C:', counter, 'M:', member, 'G:', group, cmd)
    # Byte 0 - 2
    msg = (device_type << 16) | device_id

    # Weird member offset, 0 = all
    if member != 0:
        member += 7
    # Byte 3
    msg = (msg << 4) | counter
    msg = (msg << 4) | member

    if cmd == 'stop':
        cmd_nibble = 3
    elif cmd == 'up':
        cmd_nibble = 4
    else:
        cmd_nibble = 5

    # Byte 4
    msg = (msg << 4) | group
    msg = (msg << 4) | cmd_nibble

    checksum, num = 0, msg
    for _ in range(5):
        checksum += num & 0xFF
        num >>= 8
    # Byte 5
    msg = (msg << 8) | (checksum & 0xFF)  # Cut first nibble
    print('[!]', hex(msg))
    return msg

