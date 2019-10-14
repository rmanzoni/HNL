#!/bin/bash
#SBATCH -p wn
#SBATCH --time 01:00:00
#SBATCH -e $SLURM_JOB_ID.err 
#SBATCH -o $SLURM_JOB_ID.out  

echo HOME: $HOME 
echo USER: $USER 
echo SLURM_JOB_ID: $SLURM_JOB_ID
echo HOSTNAME: $HOSTNAME

# each worker node has local /scratch space to be used during job run
shopt -s expand_aliases
shopt expand_aliases
mkdir -p /scratch/$USER/${SLURM_JOB_ID}

#############################################
####### MONITORING/DEBUG INFORMATION ########
#############################################

DATE_START=`date +%s`
echo "Job started at " `date`
echo "################################################################"
TOPWORKDIR=/scratch/`whoami`
JOBDIR=slurm-job-$SLURM_JOB_ID
WORKDIR=$TOPWORKDIR/$JOBDIR
SUBMISIONDIR=/work/vstampf/CC7/CMSSW_10_4_0_patch1/src/CMGTools/HNL/cfg/test_slurm
if test -e "$WORKDIR"; then
   echo "ERROR: WORKDIR ($WORKDIR) already exists! Aborting..." >&2
   exit 1
fi
mkdir -p $WORKDIR
if test ! -d "$WORKDIR"; then
   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2
   exit 1
fi

#############################################
###### THIS IS THE ACTUAL COMPUTATION #######
#############################################

#source $VO_CMS_SW_DIR/cmsset_default.sh
source /swshare/cms/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc481
#cd $CMSSW_BASE/src
cd /work/vstampf/CMSSW_10_4_0_patch1/src
shopt -s expand_aliases
cmsenv
cd $WORKDIR
cp -rf $SUBMISIONDIR .
ls
cd `find . -type d | grep /`
echo 'running'
#python $CMSSW_BASE/src/PhysicsTools/HeppyCore/python/framework/looper.py pycfg.py config.pck --options=options.json
python /work/vstampf/CMSSW_10_4_0_patch1/src//PhysicsTools/HeppyCore/python/framework/looper.py pycfg.py config.pck --options=options.json
#python $CMSSW_BASE/src/CMGTools/RootTools/python/fwlite/looper.py config.pck
echo
echo 'sending the job directory back'
rm Loop/cmsswPreProcessing.root
cp -r Loop/* $SUBMISIONDIR
###########################################################################
DATE_END=`date +%s`
RUNTIME=$((DATE_END-DATE_START))
echo "################################################################"
echo "Job finished at " `date`
echo "Wallclock running time: $RUNTIME s"
rmdir  /scratch/$USER/${SLURM_JOB_ID}
exit 0
