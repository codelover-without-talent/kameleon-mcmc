"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Written (W) 2013 Heiko Strathmann
Written (W) 2013 Dino Sejdinovic
"""

from pickle import dump
from popen2 import popen2
import os
import sys
import time

class ClusterTools(object):
    cluster_output_filename="cluster_output.txt"
    cluster_error_filename="cluster_error.txt"
    qsub_filename="qsub_output.txt"
    
    @staticmethod
    def submit_experiment(experiment):
        
        filename=experiment.foldername+"experiment_instance.bin"
        f=open(filename, 'w')
        dump(experiment, f)
        f.close()
        
        command="OMP_NUM_THREADS=1 nice -n 10 python " + experiment.dispatcher_filename + " " + filename
        
        job_name = filename.split(os.sep)[-2].split(".")[0]
        walltime = "walltime=99:59:59"
        processors = "nodes=1:ppn=1"
        memory = "pmem=2gb"
        workdir = experiment.foldername
        output=experiment.foldername + ClusterTools.cluster_output_filename
        error=experiment.foldername + ClusterTools.cluster_error_filename
        
        job_string = """
        #PBS -S /bin/bash
        #PBS -N %s
        #PBS -l %s
        #PBS -l %s
        #PBS -l %s
        #PBS -o %s
        #PBS -e %s
        cd %s
        %s""" % (job_name, walltime, processors, memory, output, error, workdir, command)
    
        # send job_string to qsub
        outpipe, inpipe = popen2('qsub')
        print job_string
        inpipe.write(job_string)
        inpipe.close()
        
        job_id=outpipe.read().strip()
        outpipe.close()
        print job_id
        
        try:
            qsub_filename=experiment.experiment_dir + ClusterTools.qsub_filename
            f=open(qsub_filename, 'a')
            f.write(job_id + "\n")
            f.close()
        except IOError:
            print "could not save job id to file", qsub_filename
        
        time.sleep(0.1)
        
if __name__ == '__main__':
    """
    Delete all jobs from the provided file
    """
    if len(sys.argv)!=2:
        print "usage:", str(sys.argv[0]).split(os.sep)[-1], "<qsub_output_filename>"
        print "example:"
        print "python "  +str(sys.argv[0]).split(os.sep)[-1] + " /nfs/home1/ucabhst/kameleon_experiments/" + \
              ClusterTools.qsub_filename
        exit()
        
    filename=str(sys.argv[1])
    
    try:
        f=open(filename, 'r')
        lines=[line.strip() for line in f.readlines()]
        f.close()
    except IOError:
        print "Could not open file due to IOError"
        
    _, inpipe = popen2('qdel')
    for line in lines:
        if line!="":
            job_id=".".join(line.strip().split(".")[0:2])
            print "deleting job", job_id
            inpipe.write(job_id)
    
    inpipe.close()
