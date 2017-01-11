#!/bin/bash          
source $VO_CMS_SW_DIR/cmsset_default.sh                          # make scram available                                                                                        
#cd /localgrid/gfasanel/CMSSW_7_2_0_patch1/src/                  # your local CMSSW release                                                                                    
cd /user/gfasanel/Mass_resolution_study/
eval `scram runtime -sh`                                         # don't use cmsenv, won't work on batch                                                                       
python /user/gfasanel/Mass_resolution_study/histos_for_sigma_extra_newID_E.py -i 24
