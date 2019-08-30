# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: randerson
"""
from scripts import imex
from scripts import report
import settings as sett

def run_imex_local(sim_folder, see_log, verbose):
    imex.Imex_Local.set_exe_imex(sett.LOCAL_IMEX_EXE)    
    
    imexx = imex.Imex_Local(
              exe = sett.LOCAL_IMEX_EXE
            , path_to_dat = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.DAT_NAME 
            , folder_to_output = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx

def run_imex_remote(sim_folder, see_log, verbose):
    imex.Imex_Remote.set_exe_imex(sett.REMOTE_IMEX_EXE)    
    imex.Imex_Remote.set_exe_putt(sett.LOCAL_PUTT_EXE)
    imex.Imex_Remote.set_local_root(sett.LOCAL_ROOT)
    imex.Imex_Remote.set_user(sett.USER)
    imex.Imex_Remote.set_cluster_name(sett.CLUSTER_NAME)
    
    imexx = imex.Imex_Remote(
              path_to_dat = sett.REMOTE_ROOT / sett.RES_FOLD / sim_folder / sett.DAT_NAME 
            , folder_to_output = sett.REMOTE_ROOT / sett.RES_FOLD / sim_folder                        
            , queue_kind = sett.QUEUE_KIND
            , nr_processors = sett.NR_PROCESSORS            
            , see_log = see_log
            , verbose = verbose
            )
    imexx.run()
    return imexx

def run_report(sim_folder, verbose):
    report.Report.set_exe(sett.LOCAL_REPO_EXE)
    
    repo = report.Report(
              path_to_rep = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.REP_NAME 
            , path_to_rwd = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.RWD_NAME 
            , path_to_irf = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder / sett.IRF_NAME 
            , folder_to_output = sett.LOCAL_ROOT / sett.RES_FOLD / sim_folder
            , verbose= verbose
            )
    repo.run()    

if __name__ == '__main__':
    sim_folder = 'test'
    
    sim = run_imex_local(sim_folder, True, True)
    sim = run_imex_remote(sim_folder, True, True)
    
    while sim.is_alive():
        pass
    
    run_report(sim_folder, True)