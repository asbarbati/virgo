import structlog
from virgo.providers.github import GitHub

log = structlog.get_logger()


def test_provider_github():
    provider_obj = GitHub(log=log)
    metadata = provider_obj.get_metadata("ghcr.io/mirio/verbacap")
    assert metadata["data"]["parent"] == "mirio"

    metadata_error = provider_obj.get_metadata("example.com/mirio/verbacap")
    assert metadata_error["error"] == True
