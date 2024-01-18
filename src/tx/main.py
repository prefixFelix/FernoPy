import json
import network
import time
import uasyncio
import machine
from nanoweb import Nanoweb, HttpError, send_file
import tx_config
import fernotron

counter = 1
tx = machine.Pin(tx_config.general['tx_pin'], machine.Pin.OUT)

def connect():
    # Disable AP - why???
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(tx_config.general['essid'], tx_config.general['password'])
    print(f'\n\n\n[>] Connecting to {tx_config.general["essid"]}', end='')
    while not sta_if.isconnected():
        print('.', end='')
        time.sleep(0.2)
    print(f'connected with the IP {sta_if.ifconfig()[0]}!')


naw = Nanoweb()
@naw.route("/api/config")
async def get_tx_config(request):
    response = {'remotes': []}
    for remotes in tx_config.fernotron:
        response['remotes'].append(remotes['groups'])

    if request.method != "GET":
        raise HttpError(request, 501, "Methode not supported!")

    await request.write("HTTP/1.1 200 Ok\r\n")
    await request.write("Content-Type: application/json\r\n\r\n")
    await request.write(json.dumps(response).encode())


@naw.route("/api/cmd")
async def command(request):
    global counter
    await request.write("HTTP/1.1 200 Ok\r\n")

    if request.method != "POST":
        raise HttpError(request, 501, "Methode not supported!")
    try:
        content_length = int(request.headers['Content-Length'])
        content_type = request.headers['Content-Type']
    except KeyError:
        raise HttpError(request, 400, "Bad Request")

    data = (await request.read(content_length)).decode()

    if content_type == 'application/json':
        data_json = json.loads(data)
    elif content_type == 'application/x-www-form-urlencoded':
        data_json = {}
        for chunk in data.split('&'):
            key, value = chunk.split('=', 1)
            data_json[key] = value
    else:
        print('ERROR: JSON')

    # Get device type and id
    remote_num = int(data_json['remote'])
    device_type = tx_config.fernotron[remote_num]['device_type']
    device_id = tx_config.fernotron[remote_num]['device_id']

    # Exec command
    msg_hex = fernotron.build_msg(device_type, device_id, counter, int(data_json['member']), int(data_json['group']), data_json['cmd'])
    msg_bits = fernotron.convert_to_bits(msg_hex)
    fernotron.send_msg(msg_bits, tx_config.general['tx_repeat'], tx)

    # Skip 0 counter
    if counter > 15:
        counter = 1
    counter += 1

@naw.route("/")
async def index(request):
    await request.write("HTTP/1.1 200 Ok\r\n")

    await send_file(
        request,
        f'./{tx_config.general["html_assets"]}/index.html',
    )


if __name__ == '__main__':
    tx.value(0)

    connect()
    print('[!] You can now exit the shell with Crtl-x.')
    print('[!] MSGs transmitted:')

    loop = uasyncio.get_event_loop()
    loop.create_task(naw.run())
    loop.run_forever()

