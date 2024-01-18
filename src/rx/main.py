import gc
import machine
from array import array
from time import ticks_us
import rx_config


def fill(s, t, n):
    return t*(n - len(s)) + s

def rev(s):
    r = ""
    for c in s:
        r = c + r
    return r

def to_hex(candidates):
    # Find most frequent block
    block = max(set(candidates), key=candidates.count)

    block_hex = fill(hex(int(block, 2)), '0', 2)
    return block_hex

def tribit_to_bit(bits):
    sequence = ''
    for i in range(0, len(bits), 3):
        if bits[i:i+3] == '110':
            sequence += '0'
        else:
            sequence += '1'
    return sequence


def edge_to_tribit(edge_times, symbol_length, margin):
    bits = ''
    current_symbol = '1'
    for i, edge_t in enumerate(edge_times):
        #  Single symbol
        if symbol_length - margin < edge_t < symbol_length + margin:
            bits += current_symbol
        # Double symbol
        elif (symbol_length * 2) - margin < edge_t < (symbol_length * 2) + margin:
            bits += current_symbol * 2
        # Block gap
        elif (symbol_length * 8) - margin < edge_t < (symbol_length * 8) + margin:
            bits += 'SG'
        # Message gap
        elif edge_t > (symbol_length * 8) + margin:
            bits += 'BG'
        # Edge time out of acceptable margin
        else:
            bits += 'E'

        if current_symbol == '1':
            current_symbol = '0'
        else:
            current_symbol = '1'
    return bits


def tribit_to_block(bits, debug):
    # Convert to right bit sequence
    if bits.count('0SG') > bits.count('1SG'):   # End of block sign-bit as indication
        bits.replace('1', 'A')
        bits.replace('0', '1')
        bits.replace('A', '0')

    msgs = bits.split('1010101010101SG')    # Split after preamble
    gc.collect()
    if len(msgs) <= 1:
        return 'No valid preamble found!', None, None

    # Extract first 3 logic blocks (6 physical) form msgs
    msgs_cut = []
    for msg in msgs:
        blocks = msg.split('SG')
        if len(blocks) != 12:   # Ignore msg with missing blocks
            continue
        msgs_cut.append(blocks[:6])

    # Extract type / id information
    candidate_blocks = [[], [], []]
    for blocks in msgs_cut:
        for i, block in enumerate(blocks):
            if block.find('E') == -1:
                s_bits = tribit_to_bit(block[:24])
                if i in (0, 1): # Block 0
                    candidate_blocks[0].append(rev(s_bits))
                if i in (2, 3): # Block 1
                    candidate_blocks[1].append(rev(s_bits))
                if i in (4, 5): # BLock 2
                    candidate_blocks[2].append(rev(s_bits))
    if debug:
        print('+-------------- Results --------------+\n')
        print(candidate_blocks)
    if len(candidate_blocks[0]) <= 1:
        return 'No valid blocks found!', None, None

    device_type = to_hex(candidate_blocks[0])
    device_id = to_hex(candidate_blocks[1]) + to_hex(candidate_blocks[2])[2:]
    return '', device_type, device_id


if __name__ == '__main__':
    conf = rx_config.general

    rx = machine.Pin(conf['rx_pin'], machine.Pin.IN)
    abs_times = array('I', (0 for _ in range(conf['n_edges'])))

    if conf['debug']:
        print(f'\n+-------------- DEBUG Info --------------+\nData GPIO pin: {conf["rx_pin"]}\nEdges to be recorded: {conf["n_edges"]}\nSymbol length: {conf["symbol_length"]}µs\nSymbol detection margin: {conf["margin"]}µs\n+----------------------------------------+')

    print(f'\n\n\n+-------------- Device ID Sniffer --------------+\n[!] Please read chapter 1.2 of the installation instructions before proceeding!\n[>] Selected data pin: GPIO {conf["rx_pin"]}\n\n[!] Position the remote. Press and hold the STOP button. Now hit ENTER to start the sniffing process.\n+----------------------------------------+')

    ready = False
    while not ready:
        input()
        print('[>] Sniffing started..', end='')
        # --- SNIFF ---
        # Credits: https://github.com/peterhinch/micropython_remote/blob/master/rx/__init__.py
        times = array('I', (0 for _ in range(conf['n_edges'])))
        gc.collect()
        i = 0
        while i < conf['n_edges']:
            v = rx()
            while v == rx():
                pass
            times[i] = ticks_us()
            i += 1
        # --- SNIFF END ---
        print('..FINISHED! You can now release the STOP button.')
        print('[>] Processing captured data...')

        # --- Data processing ---
        # Calculate edge times
        for i in range(conf['n_edges']-2):
            times[i] = (times[i+1] - times[i])

        tribits = edge_to_tribit(times, conf['symbol_length'], conf['margin'])
        gc.collect()
        if conf['debug']:
            print('+-------------- Raw bits --------------+')
            print(tribits)
            print('+--------------------------------------+')

        error, device_type, device_id = tribit_to_block(tribits, conf['debug'])
        if error is '':
            ready = True
            print(f'[!] SUCCESS! Please proceed with the installation guide and add the type / id to the config.py file.\n[>] Device type: {device_type}\n[>] Device id: {device_id}\n')
        else:
            print(f'[!] ERROR: {error} Please try again. Maybe reposition the remote/microcontroller.\n')
            gc.collect()

