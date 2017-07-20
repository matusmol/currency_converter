#!/usr/bin/env python3

__author__ = "Matus Mol"
__email__ = "matusmol93@gmail.com"

from currency_tools import CurrencyConverter
from flask import Flask, json, request, Response

app = Flask(__name__)


def check_size(values):
    if len(values) > 3:
        raise ValueError("Minimum code size is 3")


def validate_argumets(amount, input_currency, output_currency):
    if output_currency is None:
        raise ValueError("output_currency is missing")

    if input_currency is None:
        raise ValueError("input_currency is missing")

    if amount is None:
        raise ValueError("amount is missing")

    try:
        float(amount)
    except ValueError:
        raise ValueError("amount must be float")

    check_size(input_currency)
    check_size(output_currency)


@app.route("/currency_converter")
def main():
    try:
        amount = request.args.get('amount')
        input_currency = request.args.get('input_currency')
        output_currency = request.args.get('output_currency')

        if output_currency is None:
            output_currency = ""

        validate_argumets(amount, input_currency, output_currency)

        converter = CurrencyConverter(
            float(amount), input_currency.upper(), output_currency.upper())
        result = json.loads(converter.currency_convert())
    except Exception as e:
        result = {"error": str(e)}

    return Response(json.dumps(result, sort_keys=True, indent=4), mimetype='application/json')


if __name__ == "__main__":
    app.run(port=8000)
