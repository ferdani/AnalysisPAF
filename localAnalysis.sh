
set -e 
set -o pipefail

echo "Reading samples from 'localSamples.conf'"


while read line;
do
    if [[ $line == /pool/* ]]; then
        path2=${line##*=}
        echo "changing path to " $path2
    fi

    if [ -z "$line" ]; then
        continue

    elif [[ $line != /pool/* ]]; then      
        [[ "$line" =~ ^'#'.*$ ]] && continue

        echo "path = " $path2 ";  line =  " $line 
        pwd

        root -l -b -q 'RunAnalyserPAF.C("'${line}'", "'${path2}'", "WZ", 1)'

    fi

done < localSamples.conf
