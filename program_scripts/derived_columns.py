# -*- coding: utf-8 -*-
"""
derived_columns.py

4. subscript of MPBCpipe.py

"""

############# diagnosis_vs_inclusion still needed! Below only all_dia func and calling frame work

import pandas as pd


def all_diagnoses(hvdat, dia_cols):
    hvdat["all_diagnoses"] = hvdat[dia_cols].values.tolist()
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(set)
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(list)

    # Remove missing and empty entries
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(
        lambda x: [i for i in x if pd.notna(i) and i != ""]
    )

    return hvdat

def diagnosis_vs_inclusion(... # ---------------------------------------------------------


def generate_derived_columns(qdat, hvdat, cat, cond, dia_cols):                 # func with calling framework for column generations
    # Columns user-requested for output or filtering
    qdat_cols = set(cat.get("qdat", [])) | set(cond.get("qdat", {}))            # generates a set across cat & cond
    hvdat_cols = set(cat.get("hvdat", [])) | set(cond.get("hvdat", {}))

    # All diagnoses per visit
    if "all_diagnoses" in hvdat_cols:
        hvdat = all_diagnoses(hvdat, dia_cols)

    # Diagnoses relative to inclusion: same function, different timing
    if "Doctoral_diagnoses_received_after_inclusion_year" in qdat_cols:
        qdat = diagnosis_vs_inclusion(qdat, hvdat, timing="after")              # diagnosis_vs_inclusion needed

    if "Doctoral_diagnoses_at_inclusion_+-1year" in qdat_cols:
        qdat = diagnosis_vs_inclusion(qdat, hvdat, timing="at")                 # diagnosis_vs_inclusion needed

    if "Doctoral_diagnoses_recorded_till_inclusion_+1year" in qdat_cols:
        qdat = diagnosis_vs_inclusion(qdat, hvdat, timing="upto")               # diagnosis_vs_inclusion needed


    return qdat, hvdat


