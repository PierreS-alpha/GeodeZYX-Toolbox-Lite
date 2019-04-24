# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:31:19 2016

@author: psakicki
"""

from megalib import *

# TAB STYLE 
refposdic    = collections.OrderedDict() # at 2009.0 EPOCH !!!
refveldic    = collections.OrderedDict() # at 2009.0 EPOCH !!!
newrefveldic = collections.OrderedDict() # at 2009.0 EPOCH !!!

if 0:
    refposdic['CHPH'] =  [4236233.1684  ,  110998.1464 ,  4751117.4057]    
    refposdic['MAN2'] =  [4274275.8773  ,   11584.3993  , 4718386.0750]  
    refposdic['MLVL'] =  [4201576.9075  ,  189860.1648  , 4779064.8344]  
    refposdic['SIRT'] =  [4213550.8573  ,  162494.5772  , 4769661.8199] 
    refposdic['SMNE'] =  [4201791.9923  ,  177945.5482  , 4779286.9522]
    
    refveldic['CHPH'] =  [ -0.0130      ,   0.0177      ,   0.0107  ]    
    refveldic['MAN2'] =  [ -0.0117      ,   0.0183      ,   0.0111  ]  
    refveldic['MLVL'] =  [ -0.0126      ,   0.0179      ,   0.0104  ]  
    refveldic['SIRT'] =  [ -0.0127      ,   0.0180      ,  0.0106   ] 
    refveldic['SMNE'] =  [ -0.0125       ,  0.0176       ,   0.0107  ]


refposdic['ANGL']  =  [4404491.4998,   -108110.8044,  4596491.3331] 
refposdic['AUNI']  =  [4429451.7411,    -73344.2812,  4573322.0138] 
refposdic['BRES']  =  [4370725.7209,    -36125.1712,  4629768.5816] 
refposdic['CHPH']  =  [4236233.1684,    110998.1464,  4751117.4057] 
refposdic['ILDX']  =  [4436671.0119,    -91138.0528,  4566018.1505] 
refposdic['MAN2']  =  [4274275.8773,     11584.3993,  4718386.0750] 
refposdic['ROYA']  =  [4466458.8561,    -79862.9231,  4537304.7341] 
refposdic['SMNE']  =  [4201791.9923,    177945.5482,  4779286.9522]

refposdic['BRST']  =  [4231162.5284 ,  -332746.6074 ,  4745130.9595]

refveldic['ANGL'] =   [      -0.0111    ,     0.0183    ,     0.0111]
refveldic['AUNI'] =   [      -0.0119    ,     0.0189    ,     0.0112]
refveldic['BRES'] =   [      -0.0117    ,     0.0182    ,     0.0111]
refveldic['CHPH'] =   [      -0.0130    ,     0.0177    ,     0.0107]
refveldic['ILDX'] =   [      -0.0135    ,     0.0196    ,     0.0094]
refveldic['MAN2'] =   [      -0.0117    ,     0.0183    ,     0.0111]
refveldic['ROYA'] =   [      -0.0111    ,     0.0185    ,     0.0113]
refveldic['SMNE'] =   [      -0.0125    ,     0.0176    ,     0.0107]

refveldic['BRST'] =   [      -0.0120    ,     0.0178    ,     0.0106]

FINAL_EPOCH = 2015.68 # pour test toit DPTS
FINAL_EPOCH = 2012.234972678  # pour test buoy Ile d'Aix
FINAL_EPOCH = geok.dt2year_decimal(geok.doy2dt(2016,335))  # pour test nappe Etienne P




for stat , pos in refposdic.items():
    argz = tuple(pos) + (2009.0,) + tuple(refveldic[stat]) + (FINAL_EPOCH,)
    newrefveldic[stat] = geok.itrf_speed_calc(*argz)
    
