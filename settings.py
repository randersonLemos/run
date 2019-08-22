# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:04:54 2019

@author: randerson
"""

from pathlib import Path

N_SIMS = 1

ROOT_LOCAL  = Path('U:/simulation')
MAIN_FOLDER = Path('sims')
DAT_FILE    = Path('main.dat')
IRF_FILE    = Path('main.irf')
IMEX_EXE    = Path('C:/"Program Files (x86)"/CMG/IMEX/2017.10/Win_x64/EXE/mx201710.exe')
USER = ''
QUEUE_KIND = ''
CLUSTER_NAME = ''

#MACHINE = 'local'
MACHINE = 'remote'
if MACHINE == 'remote':
    ROOT_REMOTE = Path('/home/randerson/simulation')
    IMEX_EXE = Path('/mnt/simuladores/CMG/imex/2017.10/linux_x64/exe/mx201710.exe')
    USER = 'randerson'
    CLUSTER_NAME = 'hpc02'
    QUEUE_KIND = 'longas'

REPORT_EXE = Path('C:/\"Program Files (x86)"/CMG/BR/2017.10/Win_x64/EXE/report.exe')