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
	arg_parser.add_argument('-f', '--data-file', required=True, help='.csv file or Excel spreadsheet that contains pizza club ratings.', type=str)
	arg_parser.add_argument('-o', '--output-file', required=False, help='filepath to output analysis to', type=str, default='')
	output_args: Namespace = arg_parser.parse_args()
	output_args.should_output: bool = len(output_args.output_file) > 0
	return output_args


def is_individual_ratings(data_file_name: str) -> bool:
	""" Determines if provided file name corresponds to a csv file that is individual ratings. """
	return search("[Ii]ndividual", data_file_name) != None


def get_range(data_frame: pd.DataFrame, axis: int) -> float:
	return data_frame.max(axis=axis) - data_frame.min(axis=axis)


def get_individual_analysis(data: pd.DataFrame) -> pd.DataFrame:
	""" Gets everyone's individual analysis per name, per data field """

	new_cols: typing.Dict[str, typing.Callable] = {'person_mean': pd.DataFrame.mean, 'person_range': get_range, 'person_min': pd.DataFrame.min, 'person_max': pd.DataFrame.max}
	new_rows: typing.Dict[str, typing.Callable] = {'category_mean': pd.DataFrame.mean, 'category_range': get_range, 'category_min': pd.DataFrame.min, 'category_max': pd.DataFrame.max}

	output: pd.DataFrame = data.copy()

	for col_name, col_func in new_cols.items():
		output[col_name] = col_func(data, axis=1)

	for row_name, row_func in new_rows.items():
		output.loc[row_name] = row_func(data, axis=0)

	output.loc[new_rows, new_cols] = np.nan

	return output


def get_data_file(data_filename: str) -> typing.Dict[str, pd.DataFrame]:
	if not is_excel_file(data_filename):
		return {data_filename: load_csv(data_filename)}
	return pd.read_excel(data_filename, sheet_name=None, index_col=0)


def get_analysis(data: typing.Dict[str, pd.DataFrame]) -> typing.Dict[str, pd.DataFrame]:
	output: typing.Dict[str, pd.DataFrame] = {}
	for name, sheet in data.items():
		if is_individual_ratings(name):
			analysis: pd.DataFrame = get_individual_analysis(sheet)
			output[name] = analysis
	return output


def print_analysis(data: typing.Dict[str, pd.DataFrame]):
	for name, sheet in data.items():
		print(f'Analytics for {name}:')
		print(sheet)


def write_to_file(filename: str, data: typing.Dict[str, pd.DataFrame], is_analysis: bool = False):
	with pd.ExcelWriter(filename) as excel_writer:
		for name, sheet in data.items():
			sheet_name = name + ' - Analysis' if is_analysis else name
			sheet.to_excel(excel_writer, sheet_name=sheet_name)


def main():
	arguments: Namespace = parse_args()
	data_filename: str = arguments.data_file
	data: typing.Dict[str, pd.DataFrame] = get_data_file(data_filename)
	analysis: typing.Dict[str, pd.DataFrame] = get_analysis(data)
	print_analysis(analysis)

	if arguments.should_output:
		write_to_file(arguments.output_file, analysis, is_analysis=True)


if __name__ == "__main__":
	main()
