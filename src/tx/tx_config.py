# General device configuration
general = {
    'symbol_length': 350,           # in µs
    'tx_pin': 5,                    # GPIO!
    'tx_repeat': 4,                 # MSGs transmitted per command
    'essid': 'YOUR_NETWORK_ESSID',
    'password': 'YOUR_NETWORK_PASSWORD',
    'html_assets': 'assets'         # Path to web assets
}

# Fernotron network configuration
fernotron = [
    {
        # Remote 0
        'device_type': 0x80,    # Add information from the RX scipt here!
        'device_id': 0x1234,    # Add information from the RX scipt here!
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
                'name': 'Living room',                          # Group name
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
