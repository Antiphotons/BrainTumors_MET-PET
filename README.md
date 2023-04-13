# BrainTumors_MET-PET project repository contains scientific code for analysis of the table-organized data 
# obtained from positron emission tomography image dataset proccesed by proprietary software (GE Healthcare).
# 
# The goal of project have to investigate the histospecific patterns of [11C]-Methionine kinetics in brain tumors.
# All patient data has been complitely anonymized 
#
# VCAR_csv_process.py 
# is the script that transform raw data upload from PET VCAR Software (GE AW Server) 
# to the region-of-interest (ROI) specific .txt files.
# 
# ROI_list_filler.py 
# creates the table with simplificated ROI names replacing standard PET VCAR ROI names.
#
# Curve_process.py 
# generates time-activity curves (TACs) of the ROI and measures dynamic curve parameters.
#
# Curve_statistics.py 
# generates group-averaged TACs and calculates between-group statistics for the different tumor types.
#
# FDR&FWER.py
# is needed for calculation of multiple-testing hypothesis correction.
#
# Patient_list_sorted.csv
# is the table with clinical and demography patient data.
#
# Output folder contains table and graphic output data.
#
