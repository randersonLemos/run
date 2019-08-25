# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import utils
import settings as sett

sim_folder = 'test'
folder_to_dat = utils.right_root() / sett.MAIN_FOLDER / sim_folder / sett.DAT_FILE
folder_to_output_imex = utils.right_root() / sett.MAIN_FOLDER / sim_folder   
folder_to_irf = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder / sett.IRF_FILE
folder_to_output_report = sett.ROOT_LOCAL / sett.MAIN_FOLDER / sim_folder

sim = utils.run_simulation(folder_to_dat, folder_to_output_imex)

while sim.is_alive():
    pass

utils.generate_report(folder_to_irf, folder_to_output_report)
