#!/usr/bin/env python3

__author__ = "Matus Mol"
__email__ = "matusmol93@gmail.com"

import requests
import json

# global variables
symbols_url = "http://www.localeplanet.com/api/auto/currencymap.json"
LENGHT_SYMBOL = 1
CONVERTOR_URL_HEAD = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20("
CONVERTOR_URL_BACK = ")&format=json&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="


class CurrencyConverter(object):
    """
    CurrencyConverter is class whitch convert actual currency
    to all avalible currencies
    """

    def __init__(self, amount, input_currency, output_currency):
        self.amount = amount
        self.input_currency = input_currency
        self.output_currency = output_currency

        self.codes_symbols = None
        self.err_output = None
        self.json_output = None
        self.convertor_url_mid = None
        self.currency_dict = None

    def currency_convert(self):
        try:
            self.get_codes_symbols()
            self.set_currency_code()
            self.valid_currency_code()
            self.render_list_currency_code()
            self.get_currency_ticket()
            self.render_dict_currency()
            return self.get_output()

        except Exception as e:
            return self.get_error_output(e)

    def get_codes_symbols(self):
        # get currency codes and symbols
        try:
            request_output = requests.get(symbols_url)
        except Exception:
            raise ValueError("Server with symbols is not avalible")

        self.codes_symbols = json.loads(request_output.text)

    def set_currency_code(self):
        # change sybol to currency code
        if len(self.input_currency) == LENGHT_SYMBOL:
            self.input_currency = self.replace_symbol_to_code(
                self.input_currency)

        if self.output_currency != "" and len(self.output_currency) == LENGHT_SYMBOL:
            self.output_currency = self.replace_symbol_to_code(
                self.output_currency)

    def valid_currency_code(self):
        # validating currency code argument
        if self.input_currency not in self.codes_symbols:
            raise ValueError(
                "Can\'t find currency with code " + self.input_currency)

        if self.output_currency != "" and self.output_currency not in self.codes_symbols:
            raise ValueError(
                "Can\'t find currency with code " + self.output_currency)

    def replace_symbol_to_code(self, symbol):
        # replace symbol with code
        for currency in self.codes_symbols:
            if symbol in self.codes_symbols[currency]["symbol"]:
                return self.codes_symbols[currency]["code"]
                break
        else:
            raise ValueError("Can\'t find currency for " + symbol)

    def render_list_currency_code(self):
        # creating list with pairs currency codes to convert
        convertor_url_mid = ""
        if self.output_currency != "":
            convertor_url_mid = '"' + self.input_currency + self.output_currency + '"'
        else:
            for currency in self.codes_symbols:
                if self.input_currency == self.codes_symbols[currency]["code"]:
                    continue

                convertor_url_mid += '"' + self.input_currency + \
                    self.codes_symbols[currency]["code"] + '", '

            convertor_url_mid = convertor_url_mid[:-2]

        self.convertor_url_mid = convertor_url_mid

    def get_currency_ticket(self):
        # get list of currency card
        try:
            request_output = requests.get(
                CONVERTOR_URL_HEAD + self.convertor_url_mid + CONVERTOR_URL_BACK)
        except Exception:
            raise ValueError("Server with currency is not avalible")

        self.currency_ticket = json.loads(request_output.text)

    def render_dict_currency(self):
        #  formatting of currency card
        currency_dict = {}
        if self.output_currency == "":
            for currency in self.currency_ticket['query']['results']['rate']:
                code = currency['id'][3:]
                currency_dict[code] = self.calculate_price(currency['Rate'])

        else:
            code = self.currency_ticket['query']['results']['rate']['id'][3:]
            currency_dict[code] = self.calculate_price(
                self.currency_ticket['query']['results']['rate']['Rate'])
        self.currency_dict = currency_dict

    def calculate_price(self, amount):
        if amount == "N/A":
            amount = 0.0

        return round(float(amount) * self.amount, 2)

    def get_output(self):
        output_dict = {"input":
                       {"amount": self.amount,
                        "currency": self.input_currency},
                       "output": self.currency_dict}
        return json.dumps(output_dict, sort_keys=True, indent=4)

    def get_error_output(self, error_msg):
        output_dict = {"error": str(error_msg)}
        return json.dumps(output_dict, sort_keys=True, indent=4)
