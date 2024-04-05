import gspread  # https://docs.gspread.org/en/latest/user-guide.html

from services.json_utils import load_json, load_json_links


def google_insta():
    gc = gspread.service_account_from_dict(load_json())
    sht2 = gc.open_by_url(load_json_links()).sheet1  # Open a sheet from a spreadsheet in one go
    sht2.update([[1, 2], [3, 4]], 'A1')  # Update a range of cells using the top left corner address
    sht2.update([["Как так?"]], 'B15')  # Or update a single cell
    sht2.format('A1:B1', {'textFormat': {'bold': True}})  # Format the header


if __name__ == "__main__":
    google_insta()
