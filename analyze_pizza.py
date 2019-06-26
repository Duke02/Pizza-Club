#!/usr/bin/env python3

import numpy as np
import pandas as pd
from argparse import Namespace, ArgumentParser
from re import search
import typing


def load_csv(file_name: str) -> pd.DataFrame:
	""" Loads and prunes the desired csv. """
	output: pd.DataFrame = pd.read_csv(file_name, index_col=0)
	return output


def parse_args() -> Namespace:
	arg_parser = ArgumentParser(description='Analyze Pizza Club ratings.')
	arg_parser.add_argument('-f', '--data-file', required=True, help='.csv file that contains pizza club ratings.', type=str)
	return arg_parser.parse_args()


def is_individual_ratings(data_file_name: str) -> bool:
	""" Determines if provided file name corresponds to a csv file that is individual ratings. """
	return search("[Ii]ndividual", data_file_name) != None


def get_individual_analysis(data: pd.DataFrame) -> pd.DataFrame:
	""" Gets everyone's individual analysis per name, per data field """
	new_cols: typing.List[str] = ["person_mean", "person_range", "person_min", "person_max"]
	new_rows: typing.List[str] = ["category_mean", "category_min", "category_max", "category_range"]

	output: pd.DataFrame = data
	output["person_mean"] = data.mean(axis=1)
	output["person_range"] = data.max(axis=1) - data.min(axis=1)
	output["person_min"] = data.min(axis=1)
	output["person_max"] = data.max(axis=1)

	output.loc["category_mean"] = data.mean(axis=0)
	output.loc["category_min"] = data.min(axis=0)
	output.loc["category_max"] = data.max(axis=0)
	output.loc["category_range"] = data.max(axis=0) - data.min(axis=0)

	output.loc[new_rows, new_cols] = np.nan

	return output


def main():
	arguments: Namespace = parse_args()
	data: pd.DataFrame = load_csv(arguments.data_file)
	if is_individual_ratings(arguments.data_file):
		analytics = get_individual_analysis(data)
		print(analytics)
	else:
		print("Is pizza ratings!")


if __name__ == "__main__":
	main()
