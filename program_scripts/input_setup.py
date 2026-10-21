# -*- coding: utf-8 -*-
"""
setup.py

1. subscript of MPBCpipe.py

"""

import argparse

def parse_arguments():
    # Set up argument parser
    parser = argparse.ArgumentParser()                                          # object handling command line args

    parser.add_argument("-q", "--qdat")                                         # adding obtions to the object
    parser.add_argument("-p", "--pdat")
    parser.add_argument("-hd", "--hdat")
    parser.add_argument("-v", "--vdat")
    parser.add_argument("-cat", "--categories", required=True)
    parser.add_argument("-cond", "--conditions", required=True)
    parser.add_argument("-o", "--output")
    parser.add_argument("-s", "--sort", type=str, nargs="+",
                        help="Column to sort by")
    parser.add_argument("-pt", "--pharma", nargs="*", default=None,
                        help="Pharma pick ups summary table (optional: upto/at/after)")
    parser.add_argument("-ptf", "--pharmafiltered", nargs="*", default=None,
                        help="Filtered pharma pick ups summary table (optional: upto/at/after)")
    parser.add_argument("-dt", "--diagnosis", nargs="*", default=None,
                        help="Diagnosis cases summary table")

    return parser.parse_args()                                                  # calls and checks args from command line




def setup_flags(args):
    # Assign flag arguments and checks
    
    # -s Column sorter
    sortby = args.sort if args.sort is not None else []

    # -dt -pt -ptf Table requests
    dt = args.diagnosis is not None
    pt = args.pharma is not None
    ptf = args.pharmafiltered is not None
    
    # pt / ptf med collection time filter (stores upto, at, or after)
    if pt:
        pt_time_filter = args.pharma[0] if args.pharma else None
    elif ptf:
        pt_time_filter = args.pharmafiltered[0] if args.pharmafiltered else None
    else:
        pt_time_filter = None

    # pt ptf conflict
    if pt and ptf:
        raise SystemExit("Please choose either -pt or -ptf.")

    # Check if qdat is provided
    if not args.qdat:
        raise SystemExit("Please provide questionnaire data.")

    if dt and not args.hdat and not args.vdat:
        raise SystemExit("Please provide diagnosis data or remove the -dt flag.")

    if (pt or ptf) and not args.pdat:
        raise SystemExit("Please provide pharmacy data or remove the -pt/-ptf flag.")


    return sortby, pt_time_filter