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


def is_excel_file(data_file: str) -> bool:
	return 'xls' in data_file[-5:]


def parse_args() -> Namespace:
	arg_parser = ArgumentParser(description='Analyze Pizza Club ratings.')
	arg_parser.add_argument('-f', '--data-file', required=True, help='.csv file that contains pizza club ratings.', type=str)
	output_args: Namespace = arg_parser.parse_args()
	return output_args


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


def get_data_file(data_filename: str) -> typing.Dict[str, pd.DataFrame]:
	if not is_excel_file(data_filename):
		return {data_filename: load_csv(data_filename)}
	return pd.read_excel(data_filename, sheet_name=None, index_col=0)


def print_analysis(data: typing.Dict[str, pd.DataFrame]):
	for name, sheet in data.items():
		if is_individual_ratings(name):
			analytics: pd.DataFrame = get_individual_analysis(sheet)
			print(f'Analytics for {name}:')
			print(analytics)
		else:
			print(f'Cannot analyze {name} yet as it\'s pizza ratings')


def main():
	arguments: Namespace = parse_args()
	data_filename: str = arguments.data_file
	data: typing.Dict[str, pd.DataFrame] = get_data_file(data_filename)
	print_analysis(data)


if __name__ == "__main__":
	main()
