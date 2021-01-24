#===============================================================================
#
#                         Analysis of the TW process
#
#===============================================================================

logpath="/nfs/fanae/user/vrbouza/Documents/TFM/Queue_logs/"
ext="Normal"
logpath=$logpath$ext

workingpath="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TW ANALYSIS EXECUTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
echo ""
echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Creating jobs..."
# An=$(qsub -q proof -l nodes=1:ppn=$1 -l walltime=20:00:00 -o $logpath -e $logpath -d $workingpath -F "an $1 $2 $3" Executioner.sh)
#echo $An
# qsub -q proof -l nodes=1:ppn=$1 -l walltime=20:00:00 -o $logpath -e $logpath -d $workingpath -W depend=afterany:$An -F "ch $1 $2 $3" Executioner.sh
sbatch -p batch -c $1 -J "OldPAF" Executioner.sh "ch" $1 $2 $3
#sbatch -p short -c $1 -J "OldPAF" Executioner.sh "ch" $1 $2 $3
