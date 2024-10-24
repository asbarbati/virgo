"""Main module."""

from .config import Config


class Virgo:
    def __init__(self, config: Config) -> None:
        """Main class of the package.

        Args:
            config (Config): Virgo Config class, it will contain all the infos.

        Returns:
            None
        """
        self.config = config

    def run(self) -> None:
        print()
