# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import report
import settings as sett

def generate_report(sim_folder):
    repor = report.REPORT(
          exe = sett.REPORT_EXE
        , irf_file = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / sett.IRF_FILE
        , output_folder = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder
        , verbose = True
        )
    repor.run()
    
if __name__ == '__main__':
    for idx in range(1,101):
        sim_folder = 'sim_{:03d}'.format(idx)
        generate_report(sim_folder)