from os import getenv
from structlog._config import BoundLoggerLazyProxy
from datetime import datetime
import requests


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
        else:
            self.log.error("Github Token needed for getting the information from Github.")
            return

    def get_image_versions(self, parent: str, project: str) -> dict:
        """Query the Github API in order to get the images version availables and return a list of it.

        Args:
            parent (str): User or Orgs on Github
            project (str): Project Name on GitHub

        Returns:
            Return a dict that have image metadata like:
            {"error": <bool>, "data": [
                {"last_update": "<datetime object>",
                 "name": ['<version1>', ...]},]
            }
        """
        STATUS_CODE_OK = 200
        out = {"error": False, "data": []}
        endpoint = f"{self.endpoint}/users/{parent}/packages/container/{project}/versions"
        self.log.info(f"Getting image versions from GitHub for the User/Orgs: {parent} and project: {project}")
        req = requests.get(endpoint, headers=self.headers)
        if req.status_code != STATUS_CODE_OK:
            self.log.error(f"Request returned status code: {req.status_code}")
            out["error"] = True
        else:
            for item in req.json():
                if item["metadata"]["container"]["tags"]:
                    itemdate = datetime.strptime(item["updated_at"].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
                    out["data"].append({"last_update": itemdate, "name": item["metadata"]["container"]["tags"]})
        return out

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
        self.log.info("Getting Metadata from GitHub")
        if image_repository.startswith("ghcr"):
            ir_split = image_repository.split("/")
            out["data"]["parent"] = ir_split[1]
            out["data"]["project"] = ir_split[2]
        else:
            self.log.error("The image repository not start with ghcr.")
            out["error"] = True
        return out
