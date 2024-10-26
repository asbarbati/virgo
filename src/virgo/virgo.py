"""Main module."""

from .config import Config
from structlog._config import BoundLoggerLazyProxy


class Virgo:
    def __init__(self, config: Config, log: BoundLoggerLazyProxy) -> None:
        """Main class of the package.

        Args:
            config (Config): Virgo Config class, it will contain all the infos.
            log (BoundLoggerLazyProxy): Log class to inject into the vars. Class: structlog

        Returns:
            None
        """
        self.config = config
        self.log = log
        self.image_provider = None

    def get_image_provider(self, image_repository: str) -> dict:
        """Return container image provider.

        Args:
            image_repository (str): Container Image repository url

        Returns:
            Return a dict that have image provider name in lowercase.
            Its like: {"error": <bool>, "data": "<provider name>"}
        """
        out = {"error": False, "data": None}
        DOCKERHUB_SPLITSLASHES = 2
        image_repository = image_repository.replace("https://", "").replace("http://", "")
        matched = False

        if image_repository:
            if image_repository.startswith("ghcr.io"):
                out["data"] = "github.com"
                matched = True
            if image_repository.startswith("docker.io"):
                out["data"] = "docker.io"
                matched = True
            if len(image_repository.split("/")) <= DOCKERHUB_SPLITSLASHES:
                # Match Dockerhub default format when the hostname its not specified.
                out["data"] = "docker.io"
                matched = True
        else:
            out["error"] = True
        if not matched:
            out["data"] = "undefined"
        return out

    def run(self) -> None:
        """Main function to check repos.

        Args:
            None

        Returns:
            None
        """
        self.log.info(f"Running check named: '{self.config.name}'")
        image_provider = self.get_image_provider(self.config.image_repository)
        if not image_provider["error"]:
            self.image_provider = image_provider["data"]
        else:
            self.log.error("Image provider detecting fail, please check it.")
            return
        self.log.info(f"Image provider detected: '{self.image_provider}'")
