import requests
from flask import Flask, render_template, request
import csv
import myfunctions


app = Flask(__name__)


@app.route("/calculator/", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        data = request.form
        print(
            f'{float(myfunctions.get_currency_ask("currency_table.csv", data.get("selected_currency"))) * float(data.get("amount"))} PLN'
        )
    return render_template("calculator.html")


if __name__ == "__main__":
    myfunctions.get_currency_table()
    myfunctions.make_calculator_template(
        "currency_table.csv", "templates/calculator.html"
    )
    app.run(debug=True)
