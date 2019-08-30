# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:56:39 2019

@author: randerson
"""
import re
import subprocess
from pathlib import Path, PurePosixPath

class Imex_Local:
    exe_imex = 'NEED TO BE SET VIA SET CLASS METHOD'

    @classmethod
    def set_exe_imex(cls, exe):
        cls.exe_imex = exe
        
    def __init__(self, path_to_dat, folder_to_output, see_log, verbose):
        self.path_to_dat = Path(path_to_dat)
        self.folder_to_output = Path(folder_to_output)
        self.see_log = see_log
        self.verbose = verbose

    def run(self):
        self.folder_to_output.mkdir(parents=True, exist_ok=True)

        command = str(self.exe) +\
                  ' -f '+str(self.path_to_dat) +\
                  ' -wd '+str(self.folder_to_output) +\
                  ' -parasol 15' +\
                  ' -jacpar' +\
                  ' -log' +\
                  ' -wait'
        if self.verbose: print('command run:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, shell=True)
        if self.see_log: self.log()

    def kill(self):
        command = 'taskkill /F /T /PID {}'.format(self.process.pid)
        if self.verbose: print('command kill:\n\t{}'.format(command))
        subprocess.Popen(command, shell=True)

    def log(self):
        command  = 'sleep 1 & '
        command += 'start powershell Get-Content {} -tail 10 -wait'\
            .format(self.folder_to_output / '*.log')
        if self.verbose: print('command log:\n\t{}'.format(command))
        subprocess.Popen(command, shell=True)

    def is_alive(self):
        return True if self.process.poll() == None else False

class Imex_Remote:
    exe_imex     = 'NEED TO BE SET VIA SET CLASS METHOD'
    exe_putt     = 'NEED TO BE SET VIA SET CLASS METHOD'
    local_root   = 'NEED TO BE SET VIA SET CLASS METHOD'
    user         = 'NEED TO BE SET VIA SET CLASS METHOD'
    clsuter_name = 'NEED TO BE SET VIA SET CLASS METHOD'
    
    @classmethod
    def set_exe_imex(cls, exe):
        cls.exe_imex = exe
        
    @classmethod
    def set_exe_putt(cls, exe):
        cls.exe_putty = exe
        
    @classmethod
    def set_local_root(cls, root):
        cls.local_root = root
        
    @classmethod
    def set_user(cls, user):
        cls.user = user
        
    @classmethod
    def set_cluster_name(cls, name):
        cls.cluster_name = name
    
    def __init__(self, path_to_dat, folder_to_output, queue_kind, nr_processors, see_log, verbose):        
        self.path_to_dat = PurePosixPath(path_to_dat)
        self.folder_to_output = PurePosixPath(folder_to_output)                
        self.queue_kind = queue_kind
        self.nr_processors = nr_processors
        self.see_log = see_log        
        self.verbose = verbose        

    def run(self):
        self._to_root_local(self.folder_to_output).mkdir(parents=True, exist_ok=True)        
        
        path_to_pbs = self._handle_pbs(self.exe_imex, self.path_to_dat
            , self.path_to_dat.parent, self.folder_to_output, self.queue_kind, self.nr_processors) 
        if self.verbose: print('Path to pbs_template:\n\t{}'.format(self._to_root_local(path_to_pbs)))
        
        command = str(self.exe_putty) +\
                ' -load hpc02 qsub {}'.format(path_to_pbs)
        if self.verbose: print('command run:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        self.cluster_job_pid = re.findall(r'\d+',str(self.process.communicate()[0]))[0]
        if self.see_log: self.log()

    def is_alive(self):
        return True if self._cluster_job_status() else False

    def _cluster_job_status(self):
        command = str(self.exe_putty) +\
                ' -load {} qstat {}'.format(self.cluster_name, self.cluster_job_pid)
        if self.verbose: print('command is_alive:\n\t{}'.format(command))
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def kill(self):
        pid = self.cluster_job_pid        
        command = str(self.exe_putty) +\
                  ' -load {} qdel {}'.format(self.cluster_name, pid)
        if self.verbose: print('command kill:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, shell=True)
    
    def log(self):
        path_log = (self._to_root_local(self.folder_to_output) / (self.path_to_dat.stem + '.log'))
        path_log.touch()
        command  = 'sleep 1 & '
        command += 'start powershell Get-Content {} -tail 10 -wait'\
            .format(path_log)
        if self.verbose: print('command log:\n\t{}'.format(command))
        subprocess.Popen(command, shell=True)

    def _pbs_template(self, exe, path_to_dat, folder_to_dat, folder_to_output, queue_kind, nr_processors):
        stg  = "#!/bin/bash\n"
        stg += "#PBS -S /bin/bash\n"
        stg += "#PBS -d {}\n".format(folder_to_dat)
        stg += "#PBS -q {}\n".format(queue_kind)
        stg += "#PBS -l nodes=1:ppn={}\n".format(nr_processors)
        stg += '\n'
        stg += "{} -f {} -wd {} -jacpar -log -parasol {} -wait".format(exe, path_to_dat, folder_to_output, nr_processors)
        return stg

    def _handle_pbs(self, exe, path_to_dat, folder_to_dat, folder_to_output, queue_kind, nr_processors):                
        name_of_pbs = folder_to_dat.name
        
        path_to_qsub = (self._to_root_local(self.folder_to_output) / 'pbs')        
        path_to_qsub.mkdir(parents=True, exist_ok=True)                
        with open(path_to_qsub / name_of_pbs, 'w') as fh:
            stg = self._pbs_template( exe, path_to_dat, folder_to_dat, folder_to_output, queue_kind, nr_processors)
            if self.verbose:
                print('File {}:'.format(path_to_qsub / name_of_pbs))
                print('\t'+'\n\t'.join(stg.split('\n')))
                fh.write(stg)            
        return self.folder_to_output / 'pbs' / name_of_pbs
    
    def _to_root_local(self, path):
        return self.local_root / Path(*path.parts[4:])