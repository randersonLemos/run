# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:56:39 2019

@author: randerson
"""
import re
import subprocess
from pathlib import Path, PureWindowsPath, PurePosixPath

class _Imex_Local:
    def __init__(self, exe, dat_file, output_folder, see_log, verbose):
        self.exe = Path(exe)
        self.dat_file = Path(dat_file)
        self.output_folder = Path(output_folder)
        self.see_log = see_log
        self.verbose = verbose


    def run(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)

        command = str(self.exe.absolute()) +\
                  ' -f '+str(self.dat_file.absolute()) +\
                  ' -wd '+str(self.output_folder.absolute()) +\
                  ' -parasol 18' +\
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
            .format(self.output_folder / '*.log')
        if self.verbose: print('command log:\n\t{}'.format(command))
        subprocess.Popen(command, shell=True)


    def is_alive(self):
        return True if self.process.poll() == None else False


class _Imex_Remote:
    path_putty = Path('C:/\"Program Files (x86)"/PuTTY/plink.exe')
    root_local = Path('U:/simulation')    
    _nr_processors = {'normal':'4','longas':'12'}


    def set_path_putty(cls, path): 
        cls.path_to_putty = Path(path)
    
    
    def set_root_local(cls, path):
        cls.root_local = Path(path)            
    
    
    def __init__(self, exe, dat_file, output_folder, user, cluster_name, queue_kind, see_log, verbose):
        self.exe = PurePosixPath(exe)
        self.dat_file = PurePosixPath(dat_file)
        self.output_folder = PurePosixPath(output_folder)
        self.user = user
        self.cluster_name = cluster_name
        self.queue_kind = queue_kind
        self.see_log = see_log        
        self.verbose = verbose        
        self._some_checking()


    def _some_checking(self):
        if self.queue_kind not in ('normal', 'longas'):
            raise ValueError("value of variable 'queue_kind' must be 'normal' or 'long'.")
        if self.cluster_name not in ('hpc01', 'hpc02'):
            raise ValueError("value of variable 'cluster_name' must be 'hpc01' or 'hpc02'.")


    def run(self):
        self._to_root_local(self.output_folder).mkdir(parents=True, exist_ok=True)        
        
        nr_processors = _Imex_Remote._nr_processors[self.queue_kind]        
        path_pbs_template = self. _handle_pbs_template(self.exe, self.dat_file, self.dat_file.parent
                                                       , self.output_folder, self.queue_kind, nr_processors) 
        if self.verbose: print('pbs_template.s path:\n\t{}'.format(self._to_root_local(path_pbs_template)))
        
        command = str(_Imex_Remote.path_putty) +\
                ' -load hpc02 qsub {}'.format(path_pbs_template)
        if self.verbose: print('command run:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        self.cluster_job_pid = re.findall(r'\d+',str(self.process.communicate()[0]))[0]
        if self.see_log: self.log()


    def is_alive(self):
        return True if self._cluster_job_status() else False


    def _cluster_job_status(self):
        command = str(_Imex_Remote.path_putty) +\
                ' -load {} qstat {}'.format(self.cluster_name, self.cluster_job_pid)
        if self.verbose: print('command is_alive:\n\t{}'.format(command))
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')


    def kill(self):
        pid = self.cluster_job_pid        
        command = str(_Imex_Remote.path_putty) +\
                  ' -load {} qdel {}'.format(self.cluster_name, pid)
        if self.verbose: print('command kill:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, shell=True)
        
    
    def log(self):
        path_log = (self._to_root_local(self.output_folder) / (self.dat_file.stem + '.log'))
        path_log.touch()
        command  = 'sleep 1 & '
        command += 'start powershell Get-Content {} -tail 10 -wait'\
            .format(path_log)
        if self.verbose: print('command log:\n\t{}'.format(command))
        subprocess.Popen(command, shell=True)


    def _pbs_template(self, exe, dat_file, dat_folder, output_folder, queue_kind, nro_processors):
        stg  = "#!/bin/bash\n"
        stg += "#PBS -S /bin/bash\n"
        stg += "#PBS -d {}\n".format(dat_folder)
        stg += "#PBS -q {}\n".format(queue_kind)
        stg += "#PBS -l nodes=1:ppn={}\n".format(nro_processors)
        stg += '\n'
        stg += "{} -f {} -wd {} -jacpar -log -parasol {} -wait".format(exe, dat_file, output_folder, nro_processors)
        return stg


    def _handle_pbs_template(self, exe, dat_file, dat_folder, output_folder, queue_kind, nro_processors):                
        fname = dat_file.parent.name
        
        path_qsub = (self._to_root_local(self.output_folder) / 'qsub')        
        path_qsub.mkdir(parents=True, exist_ok=True)                
        with open(path_qsub / fname, 'w') as fh:
            stg = self._pbs_template( exe, dat_file, dat_folder, output_folder, queue_kind, nro_processors)
            if self.verbose:
                print('{} file:'.format(fname))
                print('\t'+'\n\t'.join(stg.split('\n')))
                fh.write(stg)            
        return self.output_folder / 'qsub' / fname
    
    
    def _to_root_local(self, path):
        return _Imex_Remote.root_local / Path(*path.parts[4:])       
    

class IMEX:
    def __new__(cls, machine, exe, dat_file, output_folder, user='', cluster_name='', queue_kind='', see_log=False, verbose=False):
        if machine == 'local':  return _Imex_Local(exe, dat_file, output_folder, see_log, verbose)
        if machine == 'remote': return _Imex_Remote(exe, dat_file, output_folder, user, cluster_name, queue_kind, see_log, verbose)
        assert 0, 'Bad name {}'.format(machine)