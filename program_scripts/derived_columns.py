# -*- coding: utf-8 -*-
"""
derived_columns.py

4. subscript of MPBCpipe.py

"""

import pandas as pd
import re



def all_diagnoses(hvdat, dia_cols):
    hvdat["all_diagnoses"] = hvdat[dia_cols].values.tolist()
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(set)
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(list)

    # Remove missing and empty entries
    hvdat["all_diagnoses"] = hvdat["all_diagnoses"].apply(
        lambda x: [i for i in x if pd.notna(i) and i != ""]
    )

    return hvdat



def diagnosis_vs_inclusion(qdat, hvdat, dia_cols, timing, years, col):
    # Assign patient's inclusion year and match visits
    year = qdat.set_index("StudieID")["Inclusion_Year"].astype("Int64")         # assigns inclusion year to StudieID
    visit_year = hvdat["INDATUMA"].astype("string").str[:4].astype("Int64")     # series containing the years for the visits
    incl_year = hvdat["StudieID"].map(year)                                     # get incl year for the StudieID via "year"

    # Select the requested time frame
    if timing == "after":
        mask = visit_year > incl_year + years
    elif timing == "at":
        mask = (visit_year - incl_year).abs() <= years
    elif timing == "till":
        mask = visit_year <= incl_year + years

    # Get diagnoses from matching visits
    result = hvdat.loc[mask, ["StudieID"] + dia_cols].copy()                    # pd frame with dias for visits within the timing condition
                                                                                # rows where mask is False are excluded from result
    # Combine diagnosis fields into one column
    result[col] = (
        result[dia_cols]
        .fillna("")
        .astype(str)
        .agg(",".join, axis=1)
        .str.replace(r"(,+)", ",", regex=True)
        .str.strip(",")
    )

    result = result[["StudieID", col]]

    # Combine visits into one row per patient
    result = result.groupby("StudieID", as_index=False).agg({col: ",".join})

    # Remove duplicates and empty entries; keep diagnoses as lists
    result[col] = result[col].apply(
        lambda entry: list(set(dia for dia in entry.split(",") if dia))
    )

    # Add the generated column to qdat
    qdat = qdat.merge(result, on="StudieID", how="left")

    return qdat



def generate_derived_columns(qdat, hvdat, cat, cond, dia_cols):                 # func with calling framework for column generations
    # Columns user-requested for output or filtering
    qdat_cols = set(cat.get("qdat", [])) | set(cond.get("qdat", {}))            # generates a set across cat & cond
    hvdat_cols = set(cat.get("hvdat", [])) | set(cond.get("hvdat", {}))

    # All diagnoses per visit
    if "all_diagnoses" in hvdat_cols:
        hvdat = all_diagnoses(hvdat, dia_cols)
        
    # Diagnoses relative to inclusion
    for col in sorted(qdat_cols):
        match = re.fullmatch(r"Diagnoses_(after|at|till)_incl_(\d+)y", col)     # searching for presence of vs incl time cols

        if match:
            # extract timing and years
            timing = match.group(1)                                             # assigning after/at/till & years to variables
            years = int(match.group(2))

            qdat = diagnosis_vs_inclusion(
                qdat, hvdat, dia_cols, timing, years, col
            )


    return qdat, hvdat


