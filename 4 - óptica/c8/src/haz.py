from pathlib import Path

WORKSHEET_2 = "BIENPERFIL 0.37m"


def main(path: Path, args: list[str]) -> None:
    match args:
        case "1":
            from src import haz_52
            haz_52.main(path)

        case "2":
            from src import haz_37
            haz_37.main(path)

        case _:
            print("No argument passed!")
