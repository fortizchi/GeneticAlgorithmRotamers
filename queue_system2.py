##  Jose Luis Cabellos, Filiberto Ortiz, and Gabriel Merino
##  Theoretical and computational chemistry group 
##  CINVESTAV-merida 
##  FUNCTION : send to gaussian  
##  LAST MODIFICATION : Wen Jan 21 2015 
##  LAST MODIFICATION : Sun Jun  5 16:34:02 CDT 2016 

import distutils.spawn
import subprocess
import re
import optparse
import math
import sys
import glob 
import time 
import os
from sys import stdout
printf = stdout.write 
from subprocess import PIPE, Popen



DEFAULT_QUEUING_SYSTEM = "PBS"

def detect_queuing_system():
    if distutils.spawn.find_executable("qsub"):
        p = subprocess.Popen(['qsub', '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 2 and '-W additional_attributes' in err:
            return 'PBS'
        p = subprocess.Popen(['qsub', '-help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if p.returncode == 0 and (out.startswith('GE') or '-hold_jid' in out):
            return "GE"
    elif distutils.spawn.find_executable("sbatch"):
        return "SLURM"
    return None

def qsub_dependents(args, jobid=None, queuing_system=DEFAULT_QUEUING_SYSTEM):
    print jobid
    if jobid is not None:
        new_args = dependent_job_args(jobid, queuing_system) + args 
    else:
        new_args = args
        print new_args 
    return qsub(new_args, queuing_system=queuing_system)

def qsub(args,iii,queuing_system=DEFAULT_QUEUING_SYSTEM):
    if queuing_system == "SLURM":
        base_cmd = "sbatch"
    else:
        base_cmd = "qsub"
    cmd = [base_cmd] + args
    ## by default print when you send 
    ii=str(iii).zfill(4)
    print "## ",ii,"  Date "+ time.strftime("%c")+" -->",args
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errmsg = p.communicate()
    if p.returncode != 0:
        raise OSError(p.returncode, "command %r failed: %s" % (" ".join(cmd), errmsg))
    return get_jobid(output, queuing_system)

def get_jobid(s, queuing_system):
    if queuing_system == "PBS":
        return s.strip()
    elif queuing_system == "GE":
        m =  re.search('Your job (?P<jobid>\d+) \("(?P<jobname>[^ "]+)"\)', s)
        if m:
            return m.group('jobid').strip()
    elif queuing_system == "SLURM":
        m =  re.search('Submitted batch job (?P<jobid>\d+)', s)
        if m:
            return m.group('jobid').strip()
    else:
        raise ValueError("Unknown queuing system %r" % queuing_system)
    return None

def dependent_job_args(jobid, queuing_system):
    templates = {'PBS':  ["-W", "depend=afterok:%s" % jobid],
                 'GE': ["-hold_jid", str(jobid)],
                 'SLURM': ["--dependency=afterok:%s" % jobid],
                 }
    return templates[queuing_system]

def qstat_lizard():
    trabajos=[]
    qs = os.popen('qstat')
    jobs = {}
    lines = qs.readlines()
    for line in lines[2:]:
        pid,job,user,time,status,queue = line.split() 
        trabajos.append(pid)
    return trabajos

def prepend_cat(filename, data, bufsize=1<<15):
    backupname = filename + os.extsep+'bak'
    try: os.unlink(backupname)
    except OSError: pass
    os.rename(filename, backupname)
    with open(filename, 'w') as outputfile: #note: outputfile's permissions lost
        p = Popen(['cat', '-', backupname], stdin=PIPE, stdout=outputfile)
        p.communicate(data)

    if p.poll() == 0:
        try: os.unlink(backupname)
        except OSError: pass

#def send2gaussian(grupos_local,ppn_local,queue_local,time_sleep_local):
def send_gaussian_inputs(grupos_local,ppn_local,queue_local,time_sleep_local,tiempocola):
    queuing_system='PBS'
    ## please don't change PBS unless you have SLURM
    time_sleep=float(time_sleep_local)
    grupos=grupos_local
    ppn=20
    ppn=ppn_local
    lizard="qgpu"
    lizard=queue_local
    args=[]   
    totaljobs=[]
    todotodo=[]
    erase_pbs=[]
    path_env=os.environ.get('PATH')
    path_env=path_env.lstrip()
    if os.path.isfile('debug'):
        print "\tDebug Mode\n"
        print " \n"
        print "\tEntering subroutine = send2gaussian"
        print " \n"
        print "Queue      =",lizard
        print "Groups     =",grupos
        print "ppn        =",ppn
        print "Time queue =",time_sleep
        print " \n"
    for file in sorted(glob.glob("*.inp")):
         base=file.split('.')
         file_gauss_out=base[0]+".out"
         if not os.path.isfile(file_gauss_out):
             fop = open(file)
             insert=0
             for line in fop:
                 if "%NprocShared=" in line:
                     insert=1
             fop.close()
             if insert == 0: 
                 string="%NprocShared="+str(ppn)+"\n"
                 prepend_cat(file,string)
                 if os.path.isfile('debug'):
                     print "Inserting ",string," to ",file
             
    for file in sorted(glob.glob("*.inp")):
        base=file.split('.')
        pbsfile=base[0]+".pbs"
        file_gauss_out=base[0]+".out"
        if not os.path.isfile(file_gauss_out):
            #print pbsfile 
            if os.path.isfile('debug'):
                print "Creating file =",pbsfile
            fh=open(pbsfile,'w')
            print >>fh, "#!/bin/bash"
            print >>fh, "%s%s" %("#PBS -N ",base[0])
            print >>fh, "%s%s" %("#PBS -l nodes=1:ppn=",str(ppn))
            print >>fh, "%s%s" %("#PBS -q ",lizard)
            pbscad="#PBS -l walltime="+tiempocola
            print >>fh, "%s" %(pbscad)
            #print >>fh, "%s" %("#PBS -l walltime=1000:00:00")
            print >>fh, "   "
            print >>fh, "cd $PBS_O_WORKDIR"
            print >>fh, "   "
            print >>fh, "%s" %("export INT=i8")
            print >>fh, "%s" %("export BINDIR=/storage/software/intel/nbo6/bin") 
            print >>fh, "%s%s%-s" %("PATH=",path_env,":/storage/software/intel/nbo6/bin")
            print >>fh, "export g09root=/storage/software/intel"
            print >>fh, "source $g09root/g09/bsd/g09.profile"
            print >>fh, "export GAUSS_SCRDIR=/scratch/$USER/$PBS_JOBNAME-$PBS_JOBID"
            print >>fh, "mkdir -p $GAUSS_SCRDIR"
            print >>fh, "   "
            print >>fh, "%s%s%s%s" %( "g09 < ",file," > ",file_gauss_out)
            print >>fh, "   "
            print >>fh, "rm -rf $GAUSS_SCRDIR" 
            fh.close()

    for file in sorted(glob.glob("*.pbs")):
        todotodo.append(file)
    todotodo.reverse()
    if len(todotodo) == 0:
        print "There are not files inp gaussian type or they already have been done"
        return 0 

    for i in reversed(range(0,len(todotodo))):
        totaljobs.append(todotodo[i])
    if os.path.isfile('debug'):
        for i in (range(0,len(totaljobs))):
              print "Job = ",i,totaljobs[i]
    encola=1
    pids=[]
    total_jobs=len(totaljobs)
    total_jobs_send=0    
    print "   "
    print "Total jobs found = ", total_jobs
    print "Enter to the pool at : Date "+ time.strftime("%c")
    print "   "
    iii=1
    while encola >= 1:
        #time.sleep(1.0) 
        time.sleep(time_sleep) 
        chamba=[]
        chamba=qstat_lizard() 
        chamba_true=[]
        for elem in pids:
            if elem in chamba:
                chamba_true.append(elem)             
        encola=len(chamba_true)
        envia=grupos-encola 
        # print "Debug=",encola,envia 
        if encola < grupos and total_jobs_send < total_jobs: 
            time.sleep(1.0) 
            encola=1 ## at least one in cola 
            lanza=[]
            lanza.append(totaljobs[total_jobs_send])
            erase_pbs.append(totaljobs[total_jobs_send])
            total_jobs_send=total_jobs_send+1
            jobid=qsub(lanza,iii,queuing_system=queuing_system)
            iii=iii+1
            pids.append(jobid)

    if not os.path.isfile('debug'):
        os.system("rm -f *.e*")
        os.system("rm -f *.o[0-9][0-9][0-9][0-9][0-9][0-9]")
        for jj in range(0,len(erase_pbs)):
            epbs=erase_pbs[jj]     
            if os.path.isfile(epbs):
                os.remove(epbs)
    else: 
        print "\tRemoving : rm -f *.e*" 
        print "\tRemoving : rm -f *.o12356789"
        os.system("rm -f *.e*")
        os.system("rm -f *.o[0-9][0-9][0-9][0-9][0-9][0-9]")
        for jj in range(0,len(erase_pbs)):
            epbs=erase_pbs[jj]   
            if os.path.isfile(epbs):
                print "\tRemoving file = ",jj,epbs 
                os.remove(epbs)
    print "Out of the pool at : Date "+ time.strftime("%c")
    return 0    

def optimize_by_dft(grupos_local,ppn_local,queue_local,time_sleep_local,tiempocola):
    queuing_system='PBS'
    ## please don't change PBS unless you have SLURM
    time_sleep=float(time_sleep_local)
    grupos=grupos_local
    ppn=20
    ppn=ppn_local
    lizard="qgpu"
    lizard=queue_local
    args=[]   
    totaljobs=[]
    todotodo=[]
    erase_pbs=[]
    path_env=os.environ.get('PATH')
    path_env=path_env.lstrip()
    if os.path.isfile('debug'):
        print "\tDebug Mode\n"
        print " \n"
        print "\tEntering subroutine = send2gaussian"
        print " \n"
        print "Queue      =",lizard
        print "Groups     =",grupos
        print "ppn        =",ppn
        print "Time queue =",time_sleep
        print " \n"
    for file in sorted(glob.glob("*.inp")):
         base=file.split('.')
         file_gauss_out=base[0]+".out"
         if not os.path.isfile(file_gauss_out):
             fop = open(file)
             insert=0
             for line in fop:
                 if "%NprocShared=" in line:
                     insert=1
             fop.close()
             if insert == 0: 
                 string="%NprocShared="+str(ppn)+"\n"
                 prepend_cat(file,string)
                 if os.path.isfile('debug'):
                     print "Inserting ",string," to ",file
             
    for file in sorted(glob.glob("*.inp")):
        base=file.split('.')
        pbsfile=base[0]+".pbs"
        file_gauss_out=base[0]+".out"
        if not os.path.isfile(file_gauss_out):
            #print pbsfile 
            if os.path.isfile('debug'):
                print "Creating file =",pbsfile
            fh=open(pbsfile,'w')
            print >>fh, "#!/bin/bash"
            print >>fh, "%s%s" %("#PBS -N ",base[0])
            print >>fh, "%s%s" %("#PBS -l nodes=1:ppn=",str(ppn))
            print >>fh, "%s%s" %("#PBS -q ",lizard)
            pbscad="#PBS -l walltime="+tiempocola
            print >>fh, "%s" %(pbscad)
            #print >>fh, "%s" %("#PBS -l walltime=1000:00:00")
            print >>fh, "   "
            print >>fh, "cd $PBS_O_WORKDIR"
            print >>fh, "   "
            print >>fh, "%s" %("export INT=i8")
            print >>fh, "%s" %("export BINDIR=/storage/software/intel/nbo6/bin") 
            print >>fh, "%s%s%-s" %("PATH=",path_env,":/storage/software/intel/nbo6/bin")
            print >>fh, "export g09root=/storage/software/intel"
            print >>fh, "source $g09root/g09/bsd/g09.profile"
            print >>fh, "export GAUSS_SCRDIR=/scratch/$USER/$PBS_JOBNAME-$PBS_JOBID"
            print >>fh, "mkdir -p $GAUSS_SCRDIR"
            print >>fh, "   "
            print >>fh, "%s%s%s%s" %( "g09 < ",file," > ",file_gauss_out)
            print >>fh, "   "
            print >>fh, "rm -rf $GAUSS_SCRDIR" 
            fh.close()

    for file in sorted(glob.glob("*.pbs")):
        todotodo.append(file)
    todotodo.reverse()
    if len(todotodo) == 0:
        print "There are not files inp gaussian type or they already have been done"
        return 0 

    for i in reversed(range(0,len(todotodo))):
        totaljobs.append(todotodo[i])
    if os.path.isfile('debug'):
        for i in (range(0,len(totaljobs))):
              print "Job = ",i,totaljobs[i]
    encola=1
    pids=[]
    total_jobs=len(totaljobs)
    total_jobs_send=0    
    print "   "
    print "Total jobs found = ", total_jobs
    print "Enter to the pool at : Date "+ time.strftime("%c")
    print "   "
    iii=1
    while encola >= 1:
        #time.sleep(1.0) 
        time.sleep(time_sleep) 
        chamba=[]
        chamba=qstat_lizard() 
        chamba_true=[]
        for elem in pids:
            if elem in chamba:
                chamba_true.append(elem)             
        encola=len(chamba_true)
        envia=grupos-encola 
        # print "Debug=",encola,envia 
        if encola < grupos and total_jobs_send < total_jobs: 
            time.sleep(1.0) 
            encola=1 ## at least one in cola 
            lanza=[]
            lanza.append(totaljobs[total_jobs_send])
            erase_pbs.append(totaljobs[total_jobs_send])
            total_jobs_send=total_jobs_send+1
            jobid=qsub(lanza,iii,queuing_system=queuing_system)
            iii=iii+1
            pids.append(jobid)

    if not os.path.isfile('debug'):
        os.system("rm -f *.e*")
        os.system("rm -f *.o[0-9][0-9][0-9][0-9][0-9][0-9]")
        for jj in range(0,len(erase_pbs)):
            epbs=erase_pbs[jj]     
            if os.path.isfile(epbs):
                os.remove(epbs)
    else: 
        print "\tRemoving : rm -f *.e*" 
        print "\tRemoving : rm -f *.o12356789"
        os.system("rm -f *.e*")
        os.system("rm -f *.o[0-9][0-9][0-9][0-9][0-9][0-9]")
        for jj in range(0,len(erase_pbs)):
            epbs=erase_pbs[jj]   
            if os.path.isfile(epbs):
                print "\tRemoving file = ",jj,epbs 
                os.remove(epbs)
    print "Out of the pool at : Date "+ time.strftime("%c")
    return 0    
