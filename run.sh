dir_path=""

while getopts 'd:' flag; do
    case "${flag}" in
        d) dir_path="${OPTARG}" ;;
    esac
done

if [ "$dir_path" = "" ]; then
    pipenv run python3 convert.py
else
    pipenv run python3 convert.py -directory dir_path
fi