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
        case "intf":
            from src import interferencia
            interferencia.main(base_path)

        # case "amplitud":
        #     from src import amplitud
        #     amplitud.main(base_path)

        # case "londa":
        #     from src import londa
        #     londa.main(base_path)

        # case "fase":
        #     from src import fase
        #     fase.main(base_path)

        case _:
            logger.error("Invalid argument")


if __name__ == "__main__":
    main()
