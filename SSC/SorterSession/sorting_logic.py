import pdb
from library.Config import Config


class Sorter:
    def __init__(self) -> None:
        config_path = 'sorting_config.ini'
        self.config = Config(filename=config_path)


if __name__ == '__main__':
    sorter = Sorter()
    pdb.set_trace()
    print(sorter.config.scoring.floor_exact_match)
