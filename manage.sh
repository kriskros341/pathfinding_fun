serve () {
    should_open_browser = 0
    echo "Open in browser?"
    options=("Yes" "No")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                should_open_browser = 1
                break;
                ;;
            "No")
                break;
                ;;
        esac
    done


    netstat=$(netstat -npta | awk '{print $4}')
    max_port=65535
    i=5000
    for ((;i<max_port;i++))
    do
        [[ ! $(netstat -atun | grep ":$i\s") ]] && {
            client_port=$i 
            break;
        }
    done
    i=$((i+1));
    echo $i
    for ((;i<max_port;i++))
    do
        [[ ! $(netstat -atun | grep "$i\s") ]] && {
            server_port=$i 
            break;
        }
    done
    echo "client started at $client_port"
    echo "server started at $server_port"
    cd front
    npx vite --port $client_port &> "/dev/null" &
    (
        if [[ should_open_browser == 1 ]]
        then
            sleep 1; xdg-open "http://localhost:$client_port/result?sp=$server_port" &> "/dev/null"
        fi
    ) & 
    cd ..
    python3 Serve.py $server_port &> "/dev/null"
    pkill -P $$
}

run_alg () {
    origin=$1
    [ ! $1 ] && {
        echo "Give origin [roman][alphabetical][natural], default Ia1"
        read origin    
        [ ! $origin ] && {
            origin="Ia1"
        }
    }
    destination=$2
    [ ! $2 ] && {
        echo "Give destination [roman][alphabetical][natural], default Ve5"
        read destination
        [ ! $destination ] && {
            destination="Ve5"
        }
    }

    algorithms=("Flood" "Astar")
    select opt in "${algorithms[@]}"
    do
        case $opt in
            "Flood")
                alg=0
                break;
                ;;
            "Astar")
                alg=1
                break;
                ;;
        esac
    done

    [ -f result.txt ] && [ -f result.detailed.json ] && {
        newname=$(date -r result.txt +"%Y-%m-%d_%H-%M-%S")
        mv result.txt bups/$newname.txt
        mv result.detailed.json bups/$newname.detailed.json
    }

    c=$(python3 SpaceStation.py $origin $destination $alg)
    echo $c > result.txt
}

edit_blocked() {
    $EDITOR data.txt   
}

[ $1 ] && [ $2 ] && {
    run_alg $1 $2
}

while true
do
    options=("run" "serve" "edit blocked paths" "exit")
    select opt in "${options[@]}"
    do
        case $opt in
            "run")
                run_alg
                break;
                ;;
            "serve")
                serve
                break;
                ;;
            "exit")
                break 2;
                ;;
            "edit blocked paths")
                edit_blocked
                break;
                ;;
        esac
    done
done

