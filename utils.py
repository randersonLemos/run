# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 15:42:03 2019

@author: randerson
"""

import imex
import report
import settings as sett

def right_root():
    root = sett.ROOT_LOCAL
    if sett.MACHINE == 'remote': root = sett.ROOT_REMOTE
    return root

def run_simulation(folder_to_dat, folder_to_output):
    imexx = imex.IMEX(            
            sett.MACHINE
            , sett.IMEX_EXE
            , folder_to_dat
            , folder_to_output
            , sett.USER
            , sett.CLUSTER_NAME
            , sett.QUEUE_KIND
            , see_log = True
            , verbose = True
            )
    imexx.run()
    return imexx

def generate_report(folder_to_irf, folder_to_output):
    repor = report.REPORT(
          exe = sett.REPORT_EXE
        , irf_file = folder_to_irf
        , output_folder = folder_to_output
        , verbose = True
        )
    repor.run()