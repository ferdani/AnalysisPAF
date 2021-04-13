#!/bin/bash




SOURCE="${BASH_SOURCE[0]}"
# ./path/to/thisFile/thisFile.sh
#echo $SOURCE

RDIR="$( dirname "$SOURCE" )"
# ./path/to/thisFile/ (la ruta a este script desde donde es llamado)
#echo $RDIR

DIR="$( cd -P "$RDIR" && pwd )"
    # sigue la ruta RDIR y haz un pwd cuando llegues.
    # -P se asegura de que bash está siguiendo un camino real, no un link
    # simbolico.
echo "Hello from $DIR! I'm the bash script you just ran :D"

# Running with -q proof is only different in that it has a small time limit
# (~2h). -q batch has a 2 days limit.
qsub -q batch -l nodes=gae031.ciencias.uniovi.es:ppn=2 -F $DIR "$DIR"/send.sh
echo "ruuuning!"

