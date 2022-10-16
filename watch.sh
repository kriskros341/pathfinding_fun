#! /usr/bin/bash

#  usage: 
#  ./watch.sh [folder] [script] [...args]

dirPath=$1
shift
python3 $@
inotifywait -m -q $dirPath -e CLOSE_WRITE |
    while read -r line; do
        if cat <<< "\"$line\"" | grep -E '[[:digit:]]{4}\"'; then
            python3 $@
        fi
    done

