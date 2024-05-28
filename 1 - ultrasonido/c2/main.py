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
        case "resonancia":
            from src import resonancia
            resonancia.main(base_path)

        case "amplitud":
            from src import amplitud
            amplitud.main(base_path)

        case "distancia":
            from src import distancia
            distancia.main(base_path)

        case _:
            logger.error("Invalid argument")


if __name__ == "__main__":
    main()
