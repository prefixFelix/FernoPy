# General device configuration
general = {
    'symbol_length': 350,               # In µs
    'tx_pin': 12,                       # Data pin for the 433MHz transmitter. GPIO!
    'tx_repeat': 4,                     # Number of MSGs transmitted per command, increase in case of connection problems

    'essid': 'YOUR_NETWORK_ESSID',
    'password': 'YOUR_NETWORK_PASSWORD',
    'static_ip': {
        'enabled': False,               # Set to False to use DHCP, if false other values will be ignored
        'ip': '192.168.0.111',          # Static IP of the FenoPy device
        'subnet_mask': '255.255.255.0', # Usually this for home networks
        'gateway': '192.168.0.1',       # Your router's IP
        'dns': '8.8.8.8'                # DNS server (Google's DNS)
    },

    'html_assets': 'assets',            # Path to web assets
    'style': {
        'start_dark': True              # Start with darkmode
    }
}


# Fernotron network configuration
fernotron = [
    {
        # Remote 0
        'device_type': 0x80,    # First two digits of the sticker number
        'device_id': 0x1234,    # The the last four digits
        'groups': [
            {
                # Default group 0. Do not remove!
                'name': 'All',
                'members': ['All']
            },
            #
            # Add your existing group and members here:
            #
            {
                # Group 1 - Example
                'name': 'Living room',                                 # Group name
                'members': ['All', 'North', 'East', 'South', 'West']   # Group member names
            },
            {   # Group 2 - Example
                'name': 'Kitchen',
                'members': ['All', 'Street', 'Garden']
            },
            #
            # ...
            #
        ]
    },
    #
    # You can also add more than one remote. If not, remove this remote.
    #
    {
        # Remote 1
        'device_type': 0x80,
        'device_id': 0x5678,
        'groups': [
            {
                # Default group 0. Do not remove!
                'name': 'All',
                'members': ['All']
            },
            #
            # ...
            #
        ]
    }
]
