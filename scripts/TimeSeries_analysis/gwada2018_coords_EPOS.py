#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 14:56:41 2018

@author: psakicki
"""

from megalib import *
import matplotlib.pyplot as plt


plt.ioff()

#### Define export paths
plots_path = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1811_Repro_Gwada_18/01_Syncro_Server_TPX1/GNSS_RESULTS/EPOS/OK_mk2_good/02_plots_raw"
logsheets_path = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1811_Repro_Gwada_18/01_Syncro_Server_TPX1/METADATA/meta_log_sheets"
#export_path= "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1811_Repro_Gwada_18/GNSS_RESULTS/EPOS/OK_mk1_dry_run/02_Plots_raws"
#export_latlonfile_path= "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1806_Jordan/RAW_NEU/Jordan_latlon.txt"
#
#### Read a simple coordinate file
#p = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1806_Jordan/RAW_DATA/PPP_coordinates/2012_307_23_sta_coordinates"
#gcls.read_epos_sta_coords_mono(p)

### Read several coordinate files
pp = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1811_Repro_Gwada_18/01_Syncro_Server_TPX1/GNSS_RESULTS/EPOS/OK_mk2_good/01_PPP_coordinates/*coord*"
L = glob.glob(pp)

#
#sinex_antenna_path = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1806_Jordan/sinex_antenna/sta_antenna.JORDAN"
#DFantenna = gfc.read_sinex_bench_antenna(sinex_antenna_path)
#

#gf.create_dir(export_path)

### DISCONT FCTS PROTOTYPE
#Discont = gfc.read_station_info_time_solo(station_info_path,timeseries.stat)[0]
#Discont = gfc.read_sinex_discontinuity_solo(sinex_discont_path,timeseries.stat)[0][1:]
#Discont = gcls.sinex_bench_antenna_DF_2_disconts(DFantenna,ts.stat)
#MetaData_dico=gfc.multi_logsheet_read(logsheets_path,return_dico=True)


Ant_dico = dict()
Rec_dico = dict()

LogSheets_list = glob.glob(logsheets_path + "/*")

for ls in LogSheets_list:
    Site     = gfc.read_blocks_logsheet(ls,1)
    Rec_list = gfc.read_blocks_logsheet(ls,3)
    Ant_list = gfc.read_blocks_logsheet(ls,4)
    
    Rec_dico[Site[0].Four_Character_ID] = Rec_list
    Ant_dico[Site[0].Four_Character_ID] = Ant_list 
    
#############################



TSlist = gcls.read_epos_sta_coords_multi(L,0)  

coords_tab_stk = []

for ts in TSlist:
    nbday = (ts.enddate() - ts.startdate()).days + 1.
    print(ts.stat , ts.startdate()  , ts.enddate() , nbday , ts.nbpts , ts.nbpts * 100. / nbday )

for ts in TSlist:
    if ts.nbpts == 1:
        print(ts.stat,"excluded bc ts.nbpts == 1")
        continue
    
    ts.ENUcalc_from_mean_posi()
    
    if 1:
        std_val_lim = 0.4
        if ts.stat == "GHAJ":
            std_val_lim = 1000000
            tsGHAJ = ts
        
        ts2 = gcls.std_dev_cleaner(ts,std_val_lim,"XYZ",verbose=False)
        if ts2.nbpts == 0:
            print(ts.stat,"excluded bc ts2.nbpts == 0")
            continue
    
    if 1:
        ts3 = gcls.mad_cleaner(ts2,coortype="XYZ",
                               detrend_first=True,verbose=True)


    if 1: ### TimeWin for specific stats
        if ts.stat == "JSLM":
            ts3 = gcls.time_win(ts3,[(dt.datetime(2017,2,1),dt.datetime(2099,12,1))])
        if ts.stat == "GHAJ":
            ts3 = gcls.time_win(ts3,[(dt.datetime(2017,2,1),dt.datetime(2099,12,1))]) 
        if ts.stat == "YRCM":
            ts3 = gcls.time_win(ts3,[(dt.datetime(2016,4,5),dt.datetime(2099,12,1))]) 

    if 1: ### Add discont
        Discont_Rec = []
        Discont_Ant = []
        ### Discont = gcls.sinex_bench_antenna_DF_2_disconts(DFantenna,ts.stat)
        #Discont_Rec = [Rec.Date_Installed for Rec in Rec_dico[ts3.stat]]
        Discont_Ant = [Ant.Date_Installed for Ant in Ant_dico[ts3.stat]]
        
        Discont = sorted(Discont_Rec + Discont_Ant)
        
        ts3.set_discont(Discont)

    if 1: ### PLOT
        Fig = plt.figure()
        ts3.plot("ENU",fig=Fig)
        gcls.export_ts_plot(ts3,plots_path)
        
    if 0: # export HECTOR/MIDAS ENU files
        gcls.export_ts_as_neu(ts3, export_path , "")
        gcls.export_ts_as_midas_tenu(ts3, export_path , "")
        
    if 0: # stack lat lon in a QnD file
        coords_tab_stk.append([ts3.stat,ts3.mean_posi().L,ts3.mean_posi().F])

if 0:
    ### Export stacked lat lon
    F = open(export_latlonfile_path,"w+")
    for l in coords_tab_stk:
        F.write(gf.join_improved(" ",*l) + "\n")
    F.close()
  
