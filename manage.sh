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

c=$(python3 SpaceStation.py $origin $destination $alg)
echo $c
echo "serve results locally? y|n"
read -N 1 serve
echo ""

[[ $serve == "y" ]] && {
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
    (sleep 1; xdg-open "http://localhost:$client_port?sp=$server_port") & 
    #  GIL to SYF.
    python3 Serve.py $server_port
    pkill -P $$
}

