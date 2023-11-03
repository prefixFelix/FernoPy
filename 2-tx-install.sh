#!/bin/bash
# TX INSTALL
port=$1
echo "+-------------- Installing TX via ${port} --------------+"
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
cd src/tx
echo "$(mpremote connect "$port" cp boot.py :boot.py)"
echo "$(mpremote connect "$port" cp main.py :main.py)"
echo "$(mpremote connect "$port" cp tx_config.py :tx_config.py)"
echo "$(mpremote connect "$port" cp fernotron.py :fernotron.py)"
echo "$(mpremote connect "$port" cp nanoweb.py :nanoweb.py)"
assetsPath="assets"
echo "$(mpremote connect "$port" mkdir "$assetsPath")"
echo "$(mpremote connect "$port" cp "$assetsPath"/index.html :"$assetsPath"/index.html)"
echo "$(mpremote connect "$port" cp "$assetsPath"/style.css :"$assetsPath"/style.css)"
echo "$(mpremote connect "$port" cp "$assetsPath"/remote.js :"$assetsPath"/remote.js)"

# Start shell
echo "DONE!"
echo "+-------------- Starting FernoPy (You can exit the shell now if you want) --------------+"
mpremote connect ${port} reset
mpremote connect ${port} repl
