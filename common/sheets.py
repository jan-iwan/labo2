import gspread
from google.oauth2.service_account import Credentials
import sys
import logging
import pandas as pd
from pathlib import Path

# sheets
logger = logging.getLogger(__name__)

CREDS_PATH = Path("~/.config/gspread/labo2_SA.json").expanduser()


def open_sheet(path: Path) -> gspread.Spreadsheet:
    """
    Open a Google Sheets document.
    `path` is a directory containing a file named 'sheet-id', which has the id
    of the document.
    """

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=scopes)

    try:
        client = gspread.authorize(creds)

        logger.info("Opening `sheet-id`.")

        with open(path/"sheet-id") as id_file:
            id = id_file.read().rstrip('\n')

        logger.info(f"Using key `{id}`.")
        document = client.open_by_key(id)

        return document

    except gspread.exceptions.SpreadsheetNotFound:
        logger.error("gpread: Could not find spreadsheet.")

    except gspread.exceptions.NoValidUrlKeyFound:
        logger.error("gpread: Invalid key.")

    except gspread.exceptions.APIError:
        logger.error(
            """
            gpread: API error, It might be usage limits: For Sheets API v4 it
            is 300 requests per 60 seconds per project, and 60 requests per 60
            seconds per user.
            """)

    except gspread.exceptions.GSpreadException:
        logger.error("gpread: Something failed idk.")

    sys.exit(1)


def get_dataframe(
    ws: gspread.Worksheet,
    cellrange: str = None
) -> pd.DataFrame:
    """
    Convert a range of cells of a Google Sheets worksheet into a Pandas
    dataframe. If `cellrange` is None, the entire worksheet is converted.
    """

    if cellrange is None:
        logger.info(
            f"Getting all gspread records from worksheet '{ws.title}'.")
        return pd.DataFrame(ws.get_all_records())

    data = ws.get(cellrange)

    headers = data[0]  # Column names
    values = data[1:]  # Actual data

    # Get a list of dicts { header: values } from the list of lists
    records = gspread.utils.to_records(headers, values)

    df = pd.DataFrame(records)

    return df
