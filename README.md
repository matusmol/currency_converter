# kiwi_project
Currency converter

**Requirement**
- Flask
- Python3+

**Usage**
CLI application
- ./currency_converter.py --amount `amount` --input_currency `input_currency` --output_currency `output_currency`


**Usage**
web API application
- start server ./currency_converter_api.py
- open browser with url [http://localhost:8000/currency_converter?amount=`amount`&input_currency=`input_currency` &output_currency=`output_currency`](http://localhost:8000/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD)


**Legend**
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol

**Behavior**
- If currency curse is not available replace it with 0
- If you use symbol ¥ for argument sometimes return CNY and sometimes return JPY because Chinese yuan (CNY) and the Japanese yen (JPY) have the same symbol and this depend on witch current return symbol server first 
