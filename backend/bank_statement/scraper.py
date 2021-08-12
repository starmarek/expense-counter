import datetime
import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def getTextPdf(pdf_file):
    """
    Converts a pdf file to string.
    Input: pdf_file (format pdf)
    Output: text (string)
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(pdf_file, "rb")
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(
        fp,
        pagenos,
        maxpages=maxpages,
        password=password,
        caching=caching,
        check_extractable=True,
    ):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
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
    Input: text (string)
    Output: result (list of dictionaries)
    """
    # reduces extra new lines
    text = re.sub(r"(\n\s*)+\n", "\n\n", text).replace("\n\n", "\n")

    # cuts unnecessary information
    pages = [page[0] for page in re.findall(r"Saldo\n((.+\n)+?)(Saldo do przeniesienia|Saldo końcowe)", text)]

    pattern = re.compile(
        r"(?P<date>\d{2}\.\d{2}\.\d{4})\n([A-Z0-9]{17})\n(?P<operation_type>[^0-9]+)\n(?P<value>-?\d+,\d{2})\n(?P<balance>\d+(?: \d+)*,\d{2})\n\d{2}\.\d{2}\.\d{4}\n(?P<details>(?:(?!\d{2}\.\d{2}\.\d{4}).|\n)*)"
    )

    # get result as dictionaries of each operation
    result = [m.groupdict() for page in pages for m in pattern.finditer(page)]

    # change date format, insert time key to dictionary, remove time from category, prepare value and balance
    for row in result:
        row["date"] = datetime.datetime.strptime(row["date"], "%d.%m.%Y").strftime("%Y-%m-%d")
        time = re.search(r"Godz.(?P<time>\d{2}:\d{2})", row["details"])
        row["time"] = "00:00" if time is None else time.group("time")
        row["details"] = "".join(re.split(r" Godz.\d{2}:\d{2}:\d{2}", row["details"])).replace("\n", " ")
        row["details"] = (
            re.search(r"Lokalizacja: (.+) Nr ref:", row["details"]).group(1)
            if re.search(r"Nr ref:", row["details"])
            else row["details"]
        )
        row["value"] = round(float(row["value"].replace(" ", "").replace(",", ".")), 2)
        row["balance"] = round(float(row["balance"].replace(" ", "").replace(",", ".")), 2)

    return result


def getStatementDate(text):
    """
    Get date from statement and converts it to the django date format.
    Input: text (string)
    Output: date (string)
    """
    date = re.search(re.compile(r"Data: ((\d+).(\d+).(\d+))"), text).group(1)
    return datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")
