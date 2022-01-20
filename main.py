import argparse
import sys
from webscraper import webscrp as wp
import pandas as pd


def main():

    print("Starting extraction...")
    list_gse = wp.get_list_experiment(args.taxid)
    dict_master = wp.get_samples_series(list_gse, args.taxid)
    list_to_df = wp.dict_to_list_of_list(dict_master)
    df_remap = wp.create_df(list_to_df)
    df_remap.to_csv(args.out, index=False)
    print("Extraction finished! Dataframe saved!")


if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="A script to return a file with the GEO-NCBI samples (GSM) with their respectives SRR Ids")

    parser.add_argument(
        '-t', '--taxid', action="store",
                        help='taxid number according with NCBI to generate the api',
                        required=True)

    parser.add_argument(
        '-o', '--out', action="store",
                        help='Path to save the ReMap csv file',
                        required=True)
    
    args = parser.parse_args()
    main()
