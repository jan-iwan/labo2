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
        case "m1":
            from src import masa_1
            masa_1.main(base_path)

        case "m2":
            from src import masa_2
            masa_2.main(base_path)

        case "m3":
            from src import masa_3
            masa_3.main(base_path)

        # case "d1":
        #     from src import masa_1
        #     masa_1.main(base_path)

        case _:
            logger.error(f"Invalid argument '{arg}'.")


if __name__ == "__main__":
    main()
