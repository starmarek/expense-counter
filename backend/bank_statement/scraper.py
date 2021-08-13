import datetime
import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from backend.settings import DATE_PATTERN


def getTextPdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    with open(pdf_file, "rb") as fp:
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

    return retstr.getvalue()


def getOperations(text):
    # reduces extra new lines
    text = re.sub(r"(\n\s*)+\n", "\n\n", text).replace("\n\n", "\n")

    # cuts unnecessary information
    pages = [page[0] for page in re.findall(r"Saldo\n((.+\n)+?)(Saldo do przeniesienia|Saldo końcowe)", text)]

    # get informations about: date, operation type, value(amount), balance and details
    pattern = re.compile(
        r"(?P<date>\d{2}\.\d{2}\.\d{4})\n([A-Z0-9]{17})\n(?P<operation_type>[^0-9]+)\n(?P<value>-?\d+,\d{2})\n(?P<balance>\d+(?: \d+)*,\d{2})\n\d{2}\.\d{2}\.\d{4}\n(?P<details>(?:(?!\d{2}\.\d{2}\.\d{4}).|\n)*)"
    )

    # get result as dictionaries of each operation
    data = [m.groupdict() for page in pages for m in pattern.finditer(page)]

    # change date format, insert time key to dictionary, remove time from category, prepare value and balance
    result = []
    for row in data:
        capsule = {}
        capsule["date"] = datetime.datetime.strptime(row["date"], "%d.%m.%Y").strftime("%Y-%m-%d")
        time = re.search(r"Godz.(?P<time>\d{2}:\d{2})", row["details"])
        capsule["time"] = "00:00" if time is None else time.group("time")
        splited_details = "".join(re.split(r" Godz.\d{2}:\d{2}:\d{2}", row["details"])).replace("\n", " ")
        capsule["details"] = (
            re.search(r"Lokalizacja: (.+) Nr ref:", splited_details).group(1)
            if re.search(r"Nr ref:", splited_details)
            else splited_details
        )
        capsule["value"] = round(float(row["value"].replace(" ", "").replace(",", ".")), 2)
        capsule["balance"] = round(float(row["balance"].replace(" ", "").replace(",", ".")), 2)
        capsule["operation_type"] = row["operation_type"]
        result.append(capsule)
    return result


def getStatementDate(text):
    date = re.search(re.compile(r"Data: ((\d+).(\d+).(\d+))"), text).group(1)
    return datetime.datetime.strptime(date, "%d.%m.%Y").strftime(DATE_PATTERN)
