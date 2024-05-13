import sys
import getopt
import logging
from common import data, plot, fit

logger = logging.getLogger(__name__)


def parse(argv: list[str]) -> list[str]:
    try:
        opts, args = getopt.getopt(argv, "pvRl:dr")

    except getopt.GetoptError as err:
        logger.error(err)
        sys.exit(1)

    for opt, arg in opts:
        match opt:
            # Show plots
            case "-p":
                plot.opt_show_plots = True

            # Verbose
            case "-v":
                logging.basicConfig(level=logging.INFO)

            # Regenerate data from Google Sheets
            case "-R":
                data.opt_regen_sheets = True

            # Log file
            case "-l":
                logging.basicConfig(filename=arg)

            # Show dataframe
            case "-d":
                data.opt_show_dataframe = True

            # Show results
            case "-r":
                fit.utils.opt_show_result = True

            # Default
            case _:
                logger.error("Invalid argument.")

    return args
