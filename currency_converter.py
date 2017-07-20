#!/usr/bin/env python3

__author__ = "Matus Mol"
__email__ = "matusmol93@gmail.com"

from currency_tools import CurrencyConverter
import argparse
import json


def check_size(values):
    if len(values) > 3:
        raise argparse.ArgumentTypeError("Minimum parameter size is 3")
    return values


if __name__ == "__main__":
    try:
        # parsing argument
        parser = argparse.ArgumentParser(
            description='Real-life currency converter')
        parser.add_argument('--amount', required=True, type=float,
                            nargs=1, help='Amount which we want to convert - float')
        parser.add_argument('--input_currency', required=True, type=check_size,
                            nargs=1, help='input currency - 3 letters name or currency symbol')
        parser.add_argument('--output_currency', type=check_size, default="",
                            help='requested/output currency - 3 letters name or currency symbol')

        args = parser.parse_args()

        # call currency converter
        converter = CurrencyConverter(args.amount[0], args.input_currency[
                                      0].upper(), args.output_currency.upper())

        # get result
        result = converter.currency_convert()

        print(result)
    except Exception as e:
        # show error msg
        result = {"error": str(e)}
        print(json.dumps(result, sort_keys=True, indent=4))
