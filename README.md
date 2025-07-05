<p align="center">
<img alt="FernoPy Logo" src="img/logo.png" heigth=167 width=136/>
</p>
<h1 align="center">FernoPy</h1>

**FernoPy** enables the control of Rademacher FernoTron devices (shutters) conveniently via a web interface and REST-API.

## Features

- Responsive web interface
- REST-API (Home Assistant, ioBroker, openHAB support)
- Unlimited number of devices
- The original FernoTron remote control can be used alongside FernoPy
- Quick and easy to set up
- Cheap (total cost of only 10€)
- Covers a whole medium-sized house
- ESP32 / ESP8266 support
- Written in MicroPython
- **[Protocol documentation](PROTOCOL.md)** (not completed)

> [!NOTE]
> Only the basic control of devices is supported (up / down / stop). If you want to program devices please use: [tronferno-mcu](https://github.com/zwiebert/tronferno-mcu)

## Overview

<p align="center">
<img alt="FernoPy Logo" src="img/interface-device.png" heigth=453 width=533/>
</p>

The web interface (left figure) is provided directly via the web server of the ESP. The design and functionality of the interface is based on the original FernoTron remote control. 

- The upper left button switches between light and dark mode
- The upper right button is used to switch between multiple remote controls. You can configure as many remote controls as you like, allowing you to control an unlimited number of devices via FernoPy. However, the maximum number of groups and participants per remote control still exist in FernoPy (7 groups with 7 devices each). 
- The left two buttons control the group number and the right ones the device number (**also called member**). Each group and device can be assigned a name.
- The lower three buttons are used to control the shutters. 

### REST-API

FernoPy can be integrated into other programs by using its REST-API. This allows you to connect the shutters to central smart home systems such as Home Assistant, ioBroker or openHAB.

#### `/api/config`

This URI can be used to query all available remote controls with their groups and the respective devices by using the GET method. To be more precise: The data of the *fernotron* dictionary in the *config.py* file is returned (without the device types and id). 

```shell
$ curl -X GET http://<YOUR_ESP_IP>/api/config
{"remotes": [
	[
		{"name": "All", "members": ["All"]}, 
		{'name': 'Living room', 'members': ['All', 'North', 'East', 'South', 'West']},
		...
	], 
	[
		...
	],
]}
```

#### `/api/cmd`


This URI can be used to transmit control messages to the shutters by using the POST method. Requests with the content-type `application/json` and `application/x-www-form-urlencoded` are supported. Group and member numbers 0-7, where 0 represents all. The available commands are up, down and stop.

```shell
# application/json
$ curl -d '{"remote":0, "member":2, "group":5, "cmd":"down"}' -H "Content-Type: application/json" -X POST http://<YOUR_ESP_IP>/api/cmd

# application/x-www-form-urlencoded
$ curl -d 'remote=0&member=2&group=5&cmd="down"' -X POST http://<YOUR_ESP_IP>/api/cmd
```

## Hardware requirements

- ESP32 / ESP8266
- 433 MHz transmitter ([Amazon DE](https://www.amazon.de/s?k=433%20mhz%20sender))
- *433 MHz receiver (Not required! See text below)*

You only need an ESP32 / ESP8266 and a 433 MHz transmitter. The functionality of FernoPy was tested with a Wemos D1 mini clone and the cheapest transmitter from amazon. The 433 MHz transmitter is oft sold in combination with an receiver. A receiver is only needed if the remote doesn't contain a sticker with the *Device ID*, if you want to take a closer look at the protocol or if you want to debug. Typical type designations for the sets are "XY-MK-5V / XD-RF-5V / FS1000A" ([datasheet](https://web.archive.org/web/20231016150458/https://www.mantech.co.za/datasheets/products/HFY-J18_HFY-FST.pdf)). For the receivers, there are still the following things to consider:  

There are ones with a tunable inductor (small coil with a screw) and ones with a crystal oscillator (small metallic box). Receivers with a tunable inductor have a greater noise component, which makes it more difficult to receive a valid messages.  However, testing has shown that these are sufficient for FernoPy. Receivers with a crystal oscillator (also called superheterodyne) can nevertheless simplify the receiving process.

## Installation Linux

### 0. Flash MicroPython

Before FernoPy can be installed, the MicroPython firmware must be flashed onto the micro controller. If MicroPython is already running on your micro controller you can skip this step. A more detailed tutorial can be found [here](https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html).

1. Install the [esptool](https://github.com/espressif/esptool/) CLI. 

   ```shell
   pip install esptool
   ```

2. Download the appropriate firmware for the micro controller [here](https://micropython.org/download/). The file must be in binary format (.bin).

3. Connect the micro controller to your PC.

4. Now find out which device file is used to communicate with the micro controller. By default it should be `/dev/ttyUSB0`. Alternatively, you can also determine it via the command: `sudo dmesg | grep tty`. The output should look similar like this and give you information about the used file.

   ```shell
   $ sudo dmesg | grep tty
   [435144.714226] usb 1-1: ch341-uart converter now attached to ttyUSB0
   ```

5. Erase the flash of the micro controller.

   ```shell
   esptool.py --port /dev/ttyUSB0 erase_flash
   ```

6. Flash the MicroPython firmware.

   ```shell
   esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dout 0 ESP8266_GENERIC-<YOUR-VERSION>.bin
   ```

   Port and the name of the firmware should of course be changed by you as needed.

### 1. Install FernoPy

#### 1.1 Prepare FernoPy

1. Install the latest version of the [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) CLI.

   ```shell
   pipx install mpremote
   ```

2. Clone the FernoPy repository.

   ```shell
   git clone https://github.com/prefixFelix/fernopy.git
   ```

3. Connect the micro controller to your PC.

4. Verify that MicroPython is running properly on your micro controller by accessing the REPL prompt.

   ```shell
   mpremote connect /dev/ttyUSB0
   ```

#### 1.2 Obtain the device ID

The shutters are normally controlled by a 2411 Rademacher remote control. The remote has a unique identification number, which is required for the operation of FernoPy.

1. Open the battery compartment cover of the FernoTron remote control and remove the batteries.
2. Take a note of the number on the larger sticker below the battery direction indicator (6 digits).
   <img src="img/remote-open.png" style="width:30%; height:auto;">

##### Alternative way if there is no sticker - 433 MHz receiver

1. Connect the micro controller to the 433 MHz receiver as shown below:

   | Micro controller | 433 MHz receiver |
   | ---------------- | ---------------- |
   | GND              | GND              |
   | 5V               | VCC              |
   | GPIO5            | DATA             |

   GPIO5 is the standard pin for the data connection. If you want to use another one you have to change it in the file `/src/debug/debug_config.py`. 

2. Connect the micro controller to your PC.

3. Run the sniffing install script and follow the given instructions.
   ```shell
   mpremote connect /dev/ttyUSB0 cp -r src/debug/. :
   mpremote connect /dev/ttyUSB0
   # Press the reset button on the ESP
   ```
   
> [!IMPORTANT]
> The recording should ideally not take place in the vicinity of possible sources of interference, such as radio weather stations that also transmit on 433 MHz. The distance between the PC and the micro controller should also be maximized for the same reason (what the USB cable can offer).  Also micro controller and receiver should not be next to each other.  
> The antenna of the receiver should be parallel to the left side of the remote control. Vertically, the antenna should be in the lower third of the remote control. The distance between the remote control and the antenna should be as small as possible (they can also touch each other).  **Compare your setup with [this illustration](img/setup.jpg)**
   
> [!TIP]
> If the recording does not work even after multiple position changes, you can activate the *debug* settings in the config file and alter the *margin* value. For the changes to take effect, the install script must be rerun.  
> If a `MemoryError` occurs you can reduce the *n_edges* value in the config. You may also need to enable *debug* output there.
   

##### Alternative way if there is no sticker - SDR / URH (For experienced users)

If you have a SDR on hand, such as an RTL-SDR, you can also sniff the ID by using the software [Universal Radio Hacker](https://github.com/jopohl/urh). You can find a prepared project in the `urh` folder. It contains predefined message types and a custom decoder for the FernoTron protocol. The program also allows you to better understand the protocol structure.

#### 1.3 Configure FernoPy

1. Open the configuration file in an editor of your choice.
   ```shell
   nano src/fernopy/config.py
   ```

2. Enter the ESSID of your home network and the password in the general dict. Also specify to which GPIO the data line of the transmitter is connected.
   ```python
   # General device configuration
   general = {
       'symbol_length': 350,               # in µs
   	'tx_pin': 12,                       # Data pin for the 433MHz transmitter. GPIO!
       'tx_repeat': 4,                     # Number of MSGs transmitted per command, increase in case of connection problems
       'essid': 'YOUR_NETWORK_ESSID',
       'password': 'YOUR_NETWORK_PASSWORD',
       'static_ip': {
           'enabled': False,               # Set to False to use DHCP, if false other values will be ignored
           'ip': '192.168.0.80',          # Static IP of the FenoPy device
           'subnet_mask': '255.255.255.0', # Usually this for home networks
           'gateway': '192.168.0.1',       # Your router's IP
           'dns': '8.8.8.8'                # DNS server (Google's DNS)
       },
       'html_assets': 'assets',            # Path to web assets
       'style': {
           'start_dark': True              # Start with darkmode
       }
   }
   ```

> [!NOTE]
> The symbol length of FernoTron is actually 400µs, but 350µs are used because of the latency of the µC. You may have to adjust this value.

3. Next, the configuration of your FernoTron remote control must be entered into the fernotron list. Start by entering for each remote the type and id you got from the step 1.2.
   ```python
   fernotron = [
       {
           # Remote 0
           'device_type': 0x80,    # First two digits of the sticker number
           'device_id': 0x1234,	# The the last four digits
   		...
   ```

4. Enter all groups and their devices with their respective names. The index of the groups and devices corresponds to that of the original remote control.
> [!WARNING]
> The first group of a remote control is always the *All* group! This must not be removed! Likewise, the first device of a group (index 0) must always be *All*! You can translate the name into your own language if you wish.

   ```python
   ...		
   		'groups': [
               {
                   # Default group. Do not remove!
                   'name': 'All',
                   'members': ['All']
               },
               {
                   # Group 1 - Example
                   'name': 'Living room',                          		# Group name
                   'members': ['All', 'North', 'East', 'South', 'West']	# Group member names
               },
               {   # Group 2 - Example
                   'name': 'Kitchen',
                   'members': ['All', 'Street', 'Garden']
               },
   			...
   ```

#### 1.4 Flash FernoPy

1. Connect the micro controller to the 433 MHz transmitter and the micro controller to your PC. 
   | Micro controller | 433 MHz receiver |
   | ---------------- | ---------------- |
   | GND              | GND              |
   | 5V               | VCC              |
   | GPIO5            | DATA             |

2. Remove all files from the micro controller.
   ```shell
   mpremote connect /dev/ttyUSB0 rm -r :/
   ```

3. Copy FernoPy on the micro controller.
   ```shell
   mpremote connect /dev/ttyUSB0 cp -r src/fernopy/. :
   ```

4. Verify that everything works fine / get the IP of the ESP if you are using DHCP.
   ```shell
   mpremote connect /dev/ttyUSB0
   # Press the reset button on the ESP
   ```

5. Open the web interface by entering the displayed IP in your browser.
> [!TIP]
> You can save a short cut to FernoPy on the home screen of your smart phone. Instructions can be found [here](https://www.androidauthority.com/add-website-android-iphone-home-screen-3181682/).

## Credits

Protocol documentation - [tronferno-mcu (Bert Winkelmann)](https://github.com/zwiebert/tronferno-mcu)  
Web server - [Nanoweb (Charles R.)](https://github.com/hugokernel/micropython-nanoweb)  
Signal processing - [Micropython Remote (Peter Hinch)](https://github.com/peterhinch/micropython_remote)  
Logo - [Flaticon](https://www.flaticon.com/free-icons)

