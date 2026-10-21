# -*- coding: utf-8 -*-
"""
data_loader.py

2. subscript of MPBCpipe.py

"""

import json
import pandas as pd


def preprocess_table(table, remove_index=False):
    if table is None:
        return None                                                             # assigns None to any table not provided

    if remove_index:
        table = table.drop(columns=["Unnamed: 0"], errors="ignore")             # qdat has no header for index col
                                                                                # --> automatically named Unnamed: 0 by pandas
    return table.convert_dtypes()                                               # sets suitable data type for each col


    
def load_data(args):
    # Read original CSV files
    qdat = pd.read_csv(args.qdat) if args.qdat else None

    # Read original TXT files
    pdat = pd.read_csv(
        args.pdat, sep="\t", encoding="cp1252"
    ) if args.pdat else None

    hdat = pd.read_csv(
        args.hdat, sep="\t", encoding="cp1252", low_memory=False
    ) if args.hdat else None

    vdat = pd.read_csv(
        args.vdat, sep="\t", encoding="cp1252", low_memory=False
    ) if args.vdat else None
    

    # Read JSON files
    with open(args.categories, encoding="utf-8") as json_file:
        cat = json.load(json_file)

    with open(args.conditions, encoding="utf-8") as json_file:
        cond = json.load(json_file)

    # Preprocess tables
    qdat = preprocess_table(qdat, remove_index=True)                            # removes qdat's index col
    pdat = preprocess_table(pdat)
    hdat = preprocess_table(hdat)
    vdat = preprocess_table(vdat)

    if qdat is not None:
        qdat = qdat.rename(columns={"Id": "StudieID"})                          # rename qdat ID col

    # Combine diagnosis tables
    if hdat is not None or vdat is not None:
        hvdat = pd.concat([hdat, vdat], ignore_index=True, join="outer")        # If only hdat OR vdat, concat ignores the "None" one
                                                                                # and hvdat contains either hdat or vdat
        if hdat is not None:
            hvdat["UTDATUMA"] = hvdat["UTDATUMA"].astype("Int64")               # prevent empty entry to 1970-date conversions
    else:
        hvdat = None                                                            # if no diagnosis data provided

    return qdat, pdat, hdat, vdat, hvdat, cat, cond