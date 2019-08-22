import subprocess
from pathlib import Path

class REPORT:
    def __init__(self, exe, irf_file, output_folder, verbose=False):
        self.exe = Path(exe)
        self.irf_file = Path(irf_file)
        self.output_folder = Path(output_folder)
        self.verbose = verbose


    def run(self):
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        rwd_file_path = self._rwd_file_maker()
        command = str(self.exe)+\
                  ' /f '+str(rwd_file_path)+\
                  ' /o '+str(self.output_folder / 'main.rep')

        if self.verbose: print('command run:\n\t{}'.format(command))
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
        self.process.communicate(input=b"\n")

    def _rwd_file_maker(self):
        rwd_path = self.irf_file.parent / 'main.rwd'
        with rwd_path.open('w') as fh:  
            fh.write(self._rwd_file())
        return rwd_path

    def _rwd_file(self):
        return\
'''
** File Report

** You will need to change the file name in the following line to your simulation
** results file:


*FILES  '{}'
*OUTPUT '{}'


*LINES-PER-PAGE  50000     ** Don't have any page breaks in the table
*TABLE-WIDTH       132     **
*NO-BLANKS                 ** Always put a value (placeholder) in each column
*PRECISION           4     ** Four significant figure in data
*TIME               ON     ** No time column
*DATE               ON     ** First column will be date
*SPREADSHEET               ** Make the output columns tab separated
*TIMES-FROM 1
**LIST-PARAMETERS

*TABLE-FOR *WELLS 'PRK085'
  *COLUMN-FOR *PARAMETERS 'Oil Rate SC - Monthly' 'Cumulative Oil SC'
*TABLE-END

*TABLE-FOR *WELLS 'PRK084'
  *COLUMN-FOR *PARAMETERS 'Oil Rate SC - Monthly' 'Cumulative Oil SC'
*TABLE-END

*TABLE-FOR *WELLS 'PRK045'
  *COLUMN-FOR *PARAMETERS 'Oil Rate SC - Monthly' 'Cumulative Oil SC'
*TABLE-END

*TABLE-FOR
  *COLUMN-FOR *PARAMETERS 'Oil Recovery Factor SCTR' *SECTORS 'Entire  Field'
*TABLE-END'''.format(self.irf_file, self.output_folder / 'main.rep')
