import csv, sys, os, requests, io


def get_currency_table():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    with open("currency_table.csv", "w", newline="") as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        tablewriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        tablewriter.writeheader()
        for currency in data[0]["rates"]:
            tablewriter.writerow(currency)


def get_lines_from_file(infilename):
    if not os.path.exists(infilename):
        print(f"ERROR: Input file does not exist: {infilename}")
        sys.exit()
    with open(infilename, "r") as infile:
        lines = infile.readlines()
    return lines


def make_calculator_template(infilename, outfilename):
    lines = get_lines_from_file(infilename)
    with io.open(outfilename, "w", encoding="utf-8") as outfile:
        outfile.write(
            '<!DOCTYPE html>\n<html lang="pl">\n\t<head>\n\t\t<meta charset="utf-8">\n\t\t<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'style.css\') }}">\n\t\t<title>Calculator</title>\n\t</head>\n\t<body>\n\t\t<form>\n\t\t\t<div class="container">\n\t\t\t<label for="currency_select">Wybierz walutę:</label>\n\t\t\t<select>'
        )
        for line in lines:
            if line != lines[0]:
                line = line.split(";")
                outfile.write(f'\n\t\t\t\t<option value="{line[1]}">{line[0]}</option>')
        outfile.write(
            '\n\t\t\t</select>\n\t\t\t<input type="number" placeholder="Wprowadź ilość" name="amount" min="0" required>\n\t\t\t<button type="submit">Przelicz</button>\n\t\t\t</div>\n\t\t</form>\n\t</body>\n</html>'
        )


def get_currency_ask(infilename, code):
    lines = get_lines_from_file(infilename)
    return [line[3] for line in lines if line[1] == code][0]
