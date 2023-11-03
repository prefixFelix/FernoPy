#!/bin/bash
# RX INSTALL
port=$1
echo "+-------------- Installing RX via ${port} --------------+"
# Get all existing files
files=$(mpremote connect "$port" ls | grep '.py')
echo "$files"

# Remove all files
while IFS= read -r file || [[ -n $file ]]; do
    fileCut=$(echo "$file" | grep -oP '(?<=\S\s).*')
    fileCut=${fileCut//[$'\n\r']/}
    echo "$(mpremote connect "$port" rm "$fileCut")"
done < <(printf '%s' "$files")

# Copy files
cd src/rx
echo "$(mpremote connect "$port" cp main.py :main.py)"
echo "$(mpremote connect "$port" cp rx_config.py :rx_config.py)"

# Start shell
echo "DONE!"
echo "+-------------- Executing RX script on the µC --------------+"
mpremote connect ${port} reset
mpremote connect ${port} repl
