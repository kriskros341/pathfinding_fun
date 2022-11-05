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
    python3 Serve.py
}

