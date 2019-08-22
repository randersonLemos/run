# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import imex
import report
import settings as sett

sim_folder = 'teset'

root = sett.ROOT_LOCAL
if sett.MACHINE == 'remote': root = sett.ROOT_REMOTE
imexx = imex.IMEX(            
      sett.MACHINE
    , sett.IMEX_EXE
    , root / sett.MAIN_FOLDER / sim_folder / sett.DAT_FILE
    , root / sett.MAIN_FOLDER / sim_folder
    , sett.USER
    , sett.CLUSTER_NAME
    , sett.QUEUE_KIND
    , see_log = True
    , verbose = True
    )
imexx.run()

while imexx.is_alive():
    pass

repor = report.REPORT(
      exe = sett.REPORT_EXE
    , irf_file = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / sett.IRF_FILE
    , output_folder = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder
    , verbose = True
    )
repor.run()