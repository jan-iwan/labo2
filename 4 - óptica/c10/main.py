from common import cli_args
from pathlib import Path
import logging
import sys

logger = logging.getLogger(__name__)


def main() -> None:
    args = cli_args.parse(sys.argv[1:])

    # Absolute path of the directory of this script
    # base_path = Path(__file__).resolve().parent

    arg = args[1] if len(args) > 1 else ""

    # What to do
    match args[0]:
        case "lente":
            from src import lente
            lente.main(arg)

        case "amp":
            from src import amp
            amp.main(arg)

        case _:
            logger.error("Invalid argument")


if __name__ == "__main__":
    main()
