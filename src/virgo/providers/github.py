from os import getenv
from structlog._config import BoundLoggerLazyProxy


class GitHub:
    def __init__(self, log: BoundLoggerLazyProxy) -> None:
        """GitHub provider for getting the information from it.

        Args:
            log (BoundLoggerLazyProxy): Log class to inject into the vars. Class: structlog

        Returns:
            None
        """
        self.endpoint = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        auth_token = getenv("GITHUB_API_TOKEN", default=None)
        self.log = log
        if auth_token:
            self.headers["Authorization"] = f"Bearer {auth_token}"
            self.log.error("Github Token needed for getting the information from Github.")
            return

    def get_metadata(self, image_repository: str) -> dict:
        """Getting the GitHub metadata like user and orgs.

        Args:
            image_repository (str): Url on ghcr in order to detect the needed data.

        Returns:
            Return a dict that have image metadata like:
            {"error": <bool>, "data":
                {"parent": "<organization name or user>",
                 "project": "<project name>"}
            }
        """
        out = {"error": False, "data": {"parent": None, "project": None}}
        if image_repository.startswith("ghcr"):
            ir_split = image_repository.split("/")
            out["data"]["parent"] = ir_split[1]
            out["data"]["project"] = ir_split[2]
        else:
            out["error"] = True
        return out
