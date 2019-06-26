#!/usr/bin/env python3

import numpy as np
import pandas as pd
from argparse import Namespace, ArgumentParser

def load_csv(file_name: str) -> pd.DataFrame:
	""" Loads and prunes the desired csv. """
	output: pd.DataFrame = pd.read_csv(file_name, index_col=0)
	return output

def parse_args() -> Namespace:
	arg_parser = ArgumentParser(description='Analyze Pizza Club ratings.')
	arg_parser.add_argument('--data-file', required=True, help='.csv file that contains pizza club ratings.', type=str)
	return arg_parser.parse_args()

def main():
	arguments: Namespace = parse_args()
	data: pd.DataFrame = load_csv(arguments.data_file)
	print(data)

if __name__ == "__main__":
	main()
