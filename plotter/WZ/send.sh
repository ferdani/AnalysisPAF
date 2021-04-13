#!/bin/bash


path="$1"
cd "$path" && cd ../../     #AnalysisPAF/ en ciencias
#correr este comando en otra carpeta devuelve 
#"macro RunAnalyserPAF.C not found"


# root6!
source /cms/slc6_amd64_gcc530/external/gcc/5.3.0/etc/profile.d/init.sh;
source /cms/slc6_amd64_gcc530/external/python/2.7.11-giojec2/etc/profile.d/init.sh;
source /cms/slc6_amd64_gcc530/external/python/2.7.11-giojec2/etc/profile.d/dependencies-setup.sh;
source /cms/slc6_amd64_gcc530/external/cmake/3.5.2/etc/profile.d/init.sh;
source /opt/root6/bin/thisroot.sh

# PAF!
# source /opt/PAF/PAF_setup.sh
source /nfs/fanae/user/gonzalezm/work/PAF_git/PROOF-Analysis-Framework/PAF_setup.sh


#Yahoo
bash localAnalysis.sh
#bash mergeBigMC.sh


