from pathlib import Path
import pandas as pd
import logging
import inspect
import os

# data
logger = logging.getLogger(__name__)

opt_regen_sheets = False
opt_show_dataframe = False


def generate(
    path: Path | str,
    worksheet: str,
    cellrange: str
) -> pd.DataFrame:
    """
    Generate and save dataframe from Google Sheets
    """

    logger.warning("Fetching Google Sheets.")

    from common import sheets

    ws = sheets.open_sheet(path).worksheet(worksheet)

    logger.info("Creating dataframe.")

    # Need to test ws.get_all_records
    df = sheets.get_dataframe(
        ws,
        cellrange=cellrange
    ).dropna().astype(float)

    df.sort_values(
        df.columns[0],
        inplace=True,
    )

    return df


def find(
    path: Path,             # e.g. "exp1"
    name: str,              # Usually __name__
    wsname: str = None,     # Worksheet name
    cellrange: str = None,  # e.g. "A2:C41"
    local: bool = False     # True if Sheet is not expected to exist
) -> pd.DataFrame:
    """
    Search for dataframe in "path/data/". If it doesn't exist, or "-R" was
    passed to the program, search in Sheets; unless `nosheet` was passed as
    True. `wsname` is the name of the worksheet: if not specified, look for a
    worksheet named the same as `module`.
    """

    # Where the dataframe should be stored
    csv_file = path/f"data/{name}.csv"

    df: pd.DataFrame

    # If there is no existing dataframe (or chose to regenerate), create it
    if (not csv_file.is_file() or opt_regen_sheets) and not local:
        if not opt_regen_sheets:
            logger.warning(f"Could not find '{csv_file}'.")

        else:
            logger.info(
                f"Found '{csv_file}'. Using gspread since '-R' was passed.")

        # Create dataframe
        df = generate(
            path,
            name if not wsname else wsname,
            cellrange
        )

        # Save file. `index=False` to disable extra column.
        df.to_csv(
            csv_file,
            index=False
        )

    # Using the generated df does not work for some reason.
    logger.info(f"Reading '{csv_file}'.")
    df = pd.read_csv(csv_file)

    if opt_show_dataframe:
        print(f"Showing '{name}' dataframe:")
        print(df.to_string())

    return df


def save(
    data: dict,
    filename: Path | str = None,
    append: str = None
    # sheet: str = None
) -> None:
    """
    Simple wrapper to save results.
    """

    # Convert dictionary to dataframe
    df = pd.DataFrame(data)

    if filename is None:
        path, name = get_caller_name()

        filename = path / f"results/{name}.csv"

    if append is not None:
        new_name = f"{filename.stem}-{append}"

        filename = filename.parent / f"{new_name}.csv"

    logger.info(f"Saving file '{filename}")

    if opt_show_dataframe:
        print(f"Showing '{filename}' results dataframe:")
        print(df)

    # Save
    df.to_csv(
        filename,
        index=False
    )

    # Upload to Google Sheets
    # if sheet is not None:
    #     logger.warning("Uploading to Google Sheets.")

    #     from common import sheets


def get_caller_name():
    # Get the current stack frame
    stack = inspect.stack()

    # Find stack frame for the calling script
    for frame in stack:
        frame_path = os.path.abspath(inspect.getframeinfo(frame[0]).filename)

        if frame_path.find("common") == -1:
            path = Path(frame_path)
            parent = path.parent

            if path.parent.name == "src":
                parent = parent.parent

            return (parent, path.stem)

    return None
