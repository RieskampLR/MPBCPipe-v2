#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
MPBCpipe.py

Description:
    

User-defined functions: None
Non-standard modules: None

Procedure:
    
Input: 
Output: 

Usage: python MPBCpipe.py -q qdat.csv -p pdat.csv -hd hdat.csv -v vdat.csv -cat cats.json -cond conds.json

Version: 2.00
Date: 2026-10-12
Author: Lea Rachel Rieskamp

"""


# Imports

from input_setup import parse_arguments, setup_flags
from data_loader import load_data
from conflict_catcher import check_conflicts
from derived_columns.py import generate_derived_columns


# 1. Setup

args = parse_arguments()                                                        # get command line arguments
sortby, pt_time_filter = setup_flags(args)                                      # read and check flag inputs


# 2. Data load & preprocessing
## load data
## csv to tsv, standardise formats, column names and IDs
## merge hdat and vdat into hvdat

qdat, pdat, hdat, vdat, hvdat, cat, cond, dia_cols = load_data(args)            # returns data as pd frames (or None if not present)

                                                                                # jsons as dictionaries
# 3. Data conflict catches

check_conflicts(args, pdat, hvdat, cat, cond)


# 4. Derived columns
## Generate columns based on categories JSON

qdat, hvdat = generate_derived_columns(qdat, hvdat, cat, cond, dia_cols)        # generated cols are assigned to the table they most relate to


# 5. Filtering
## Find IDs matching all conditions, including derived-column filters

# ----------------------------------------------------------------------------------

# 6. Table generators
## Main

## Diagnosis

## Pharma



# 7. Export
# Save generated tables







