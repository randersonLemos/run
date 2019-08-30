import subprocess
from pathlib import Path

class Report:
    exe = 'NEED TO BE SET VIA SET CLASS METHOD'

    @classmethod
    def set_exe(cls, exe):
        cls.exe = exe
    
    def __init__(self, path_to_rep, path_to_rwd , path_to_irf, folder_to_output, verbose=False):
        self.path_to_rep = path_to_rep
        self.path_to_rwd = Path(path_to_rwd)
        self.path_to_irf = Path(path_to_irf)
        self.folder_to_output = Path(folder_to_output)
        self.verbose = verbose

    def run(self):
        self.folder_to_output.mkdir(parents=True, exist_ok=True)
        
        self._fix_path_of_rwd_file()
        
        command = str(self.exe)+\
                  ' /f '+str(self.path_to_rwd)+\
                  ' /o '+str(self.path_to_rep)

        if self.verbose: print('command run:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
        self.process.communicate(input=b"\n")
        
    def _fix_path_of_rwd_file(self):
        with self.path_to_rwd.open() as fh:
            content =  fh.read()
        content = content.replace('PATH_TO_FILE.IRF', str(self.path_to_irf))
        content = content.replace('PATH_TO_FILE.REP', str(self.path_to_rep))
        with self.path_to_rwd.open('w') as fh:
            fh.write(content)    