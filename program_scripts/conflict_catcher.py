# -*- coding: utf-8 -*-
"""
conflict_catcher.py

3. subscript of MPBCpipe.py

"""


def check_conflicts(args, pdat, hvdat, cat, cond):
    # -ptf needs subnamn or ATC condition for filtering
    if args.pharmafiltered is not None:
        pharma_conditions = cond.get("pdat", {})

        if "subnamn" not in pharma_conditions and "ATC" not in pharma_conditions:
            raise SystemExit(
                "Include a subnamn and/or ATC condition in your conditions JSON file, or change -ptf to -pt."
            )

    # hvdat in cat or cond but not provided
    if hvdat is None:                                                           # if only hdat OR vdat hvdat is made of one
        if "hvdat" in cat or "hvdat" in cond:
            raise SystemExit(
                "Please provide diagnosis data, or remove hvdat from your JSON files."
            )

    # pdat in cat or cond but not provided
    if pdat is None:
        if "pdat" in cat or "pdat" in cond:
            raise SystemExit(
                "Please provide pharmacy data, or remove pdat from your JSON files."
            )

