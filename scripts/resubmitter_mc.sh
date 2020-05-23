#!/bin/bash

echo "-------------------------------"
echo "        MC resubmitter         "
echo "-------------------------------"


# first step: move finished files in /finished

echo "-> checking if jobs finished or not"

mkdir finished

# for MC
for i in *Chunk*
do
   cd $i
   nbFiles=`find . -type d | wc -l`
   if [ $nbFiles == 24 ] ; then
      cd ..
      mv $i ./finished
   else
      echo $i  "not completed yet"
      cd ..
   fi
done

# for signals
for i in HN3L*
do
   cd $i
   nbFiles=`find . -type d | wc -l`
   if [ $nbFiles == 24 ] ; then
      cd ..
      mv $i ./finished
   else
      echo $i  "not completed yet"
      cd ..
   fi
done

echo "-> checking success of jobs"

# then sort the jobs between good and failed

cd ./finished
heppyMvBadChunks.py *
heppyMvGoodChunks.py *
heppyMvGoodNoChunks.py *

# then proceed to the resubmission of the failed jobs

cd ./failed

echo "-> proceeding to resubmission of failed files"

# for MC
for i in *Chunk*
do
   cd $i
   echo "job for " $i
   run_condor_simple.sh -t 1440 ./batchScript.sh
   #echo "run bash submission script"
   echo "->job resubmitted"
   #fi
   echo ""
   cd ..
done

# for signals
for i in HN3L*
do
   cd $i
   echo "job for " $i
   run_condor_simple.sh -t 1440 ./batchScript.sh
   #echo "run bash submission script"
   echo "->job resubmitted"
   #fi
   echo ""
   cd ..
done
cd ../..
echo "--> Resubmission COMPLETED"



