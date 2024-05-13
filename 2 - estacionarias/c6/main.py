from common import cli_args
from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)


def main() -> None:
    arg = cli_args.parse(sys.argv[1:])

    # Absolute path of the directory of this script
    base_path = Path(__file__).resolve().parent

    # What to do
    match arg[0]:
        case "modos":
            from src import modos
            modos.main(base_path)

        case "barrido":
            from src import barrido
            barrido.main(base_path)

        case _:
            logger.error(f"Invalid argument '{arg}'.")


if __name__ == "__main__":
    main()
