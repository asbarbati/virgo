"""Main module."""

from .config import Config
from structlog._config import BoundLoggerLazyProxy
from .providers.github import GitHub
from .providers.dockerhub import DockerHub
from .typer import TyperImageProvider, TyperDetectedVersion, TyperImageVersion
import re


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

    def get_image_provider(self, image_repository: str) -> TyperImageProvider:
        """Return container image provider.

        Args:
            image_repository (str): Container Image repository url

        Returns:
            Return a dict that have image provider object.
            Its like: {"error": <bool>, "data": "<provider object>"}
        """
        out = TyperImageProvider(error=False, data={})
        DOCKERHUB_SPLITSLASHES = 2
        image_repository = image_repository.replace("https://", "").replace("http://", "")

        if image_repository:
            if image_repository.startswith("ghcr.io"):
                out["data"] = GitHub(log=self.log)
            if image_repository.startswith("docker.io"):
                out["data"] = DockerHub(log=self.log)
            if len(image_repository.split("/")) <= DOCKERHUB_SPLITSLASHES:
                # Match Dockerhub default format when the hostname its not specified.
                out["data"] = DockerHub(log=self.log)
        else:
            out["error"] = True
        return out

    def detect_version(self, tags: TyperImageVersion) -> TyperDetectedVersion:
        """Find the latest version to apply.

        Args:
            tags (list): The list of the tags found from the remote repo.

        Returns:
            Return a dict that have version matched.
            Its like: {"error": <bool>, "data": "<matched version>"}
        """
        matched = False
        out = TyperDetectedVersion(error=False, data=None)
        for tagiter in tags:
            if matched:
                break
            for tag in tagiter["name"]:
                version = re.match(self.config.version_match, tag)
                if version:
                    matched = True
                    out["data"] = version.string
                    break
        if not matched:
            out["error"] = True
            self.log.error("Error during detecting version.")
        return out

    def run(self) -> None:
        """Main function to check repos.

        Args:
            None

        Returns:
            None
        """
        self.log.info(f"Running check named: '{self.config.name}'")
        image_provider = self.get_image_provider(self.config.image_repository)  # type: ignore
        if not image_provider["error"]:
            self.provider = image_provider["data"]
        else:
            self.log.error("Image provider detecting fail, please check it.")
            return
        self.log.info(f"Image provider detected: '{self.provider}'")
        self.log.info("Getting the image tags from the provider")
        metadata = self.provider.get_metadata(self.config.image_repository)
        if metadata["error"]:
            self.log.error("Error during getting the tags.")
            return

        tags = self.provider.get_image_versions(metadata["data"]["parent"], metadata["data"]["project"])
        if tags["error"]:
            self.log.error("Error getting the tags")
            return

        version = self.detect_version(tags=tags["data"])
        if version["error"]:
            self.log.error("Error during matching the version.")
            return

        self.log.info(f"Version matched: '{version["data"]}'")
