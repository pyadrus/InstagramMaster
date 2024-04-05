import gspread  # https://docs.gspread.org/en/latest/user-guide.html

from services.json_utils import load_json
from system.config import links


def google_insta():
    gc = gspread.service_account_from_dict(load_json())

    # Open a sheet from a spreadsheet in one go
    sht2 = gc.open_by_url(links).sheet1

    # Update a range of cells using the top left corner address
    sht2.update([[1, 2], [3, 4]], 'A1')

    # Or update a single cell
    sht2.update([["Как так?"]], 'B15')

    # Format the header
    sht2.format('A1:B1', {'textFormat': {'bold': True}})


if __name__ == "__main__":
    google_insta()
