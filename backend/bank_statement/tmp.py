import datetime
import re

from PyPDF4 import PdfFileReader


def getTextPdf(pdf_file):
    """
    Converts a pdf file to list of strings (each page as element of list).
    Input: pdf_file (format pdf)
    Output: text (list)
    """
    readpdf = PdfFileReader(pdf_file)
    text = [readpdf.getPage(page).extractText() for page in range(readpdf.getNumPages())]
    return text


def getOperations(text):
    """
    Scrap bank statement to get :
    - date operation
    - type operation
    - operations amount
    - balance after making operation
    - additional informations
    - time operation
    Input: text (list)
    Output: result (list of dictionaries)
    """
    data = [re.findall(r"Opis operacji((.|\n)*)(Saldo do przeniesienia|Saldo ko.cowe)", page) for page in text]
    pattern = re.compile(
        r"(?P<date>\d{2}\.\d{2}\.\d{4})\n([A-Z0-9]{17})\n(?P<operation_type>[^0-9]+)\n(?P<amount>-?\d+,\d{2})\n(?P<balance>\d+(?: \d+)*,\d{2})\n\d{2}\.\d{2}\.\d{4}\n(?P<category>(?:(?!\d{2}\.\d{2}\.\d{4}).|\n)*)"
    )

    pages_list = [[i for i in [row.groupdict() for row in pattern.finditer(page[0][0])]] for page in data]

    # merge pages into one list of dictionaries
    result = []
    for page in pages_list:
        result += page

    # change date format, insert time key to dictionary, remove time from category
    for row in result:
        row["date"] = datetime.datetime.strptime(row["date"], "%d.%m.%Y").strftime("%Y-%m-%d")
        time = re.search(r"Godz.(?P<time>\d{2}:\d{2})", row["category"])
        row["time"] = "00:00" if time is None else time.group("time")
        row["category"] = "".join(re.split(r" Godz.\d{2}:\d{2}:\d{2}", row["category"])).replace("\n", " ")
        row["category"] = (
            re.search(r"Lokalizacja: (.+) Nr ref:", row["category"]).group(1)
            if re.search(r"Nr ref:", row["category"])
            else row["category"]
        )
        print(row["amount"].replace(",", "."))
        exit()

    return result


def getStatementDate(text):
    """
    Get date from statement and converts it to the django date format.
    Input: text (list)
    Output: date (string)
    """
    date = re.search(re.compile(r"Data: ((\d+).(\d+).(\d+))"), text[0]).group(1)
    return datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")


data = open(r"C:\Users\legha\OneDrive\Pulpit\wyciagi\6.pdf", "rb")
getOperations(getTextPdf(data))
