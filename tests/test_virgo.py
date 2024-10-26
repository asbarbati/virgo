import structlog
from virgo.loader import Loader
from virgo.config import Config
from virgo.virgo import Virgo
from pathlib import Path

log = structlog.get_logger()


def test_imageprovider():
    loader_obj = Loader(log=log, config_file=Path("tests/assets/config.yaml"))
    config = loader_obj.read_config()["data"]["repos"][0]
    config_obj = Config()
    config_obj.load(config=config)
    virgo_obj = Virgo(config=config_obj, log=log)

    provider = virgo_obj.get_image_provider(
        image_repository=config_obj.image_repository
    )
    assert provider["data"] == "github.com"

    providerdockerhub = virgo_obj.get_image_provider(image_repository="docker.io/redis")
    assert providerdockerhub["data"] == "docker.io"

    providermissing = virgo_obj.get_image_provider(
        image_repository="example.com/provider/missing"
    )
    assert providermissing["data"] == "undefined"

    providernoimage = virgo_obj.get_image_provider(image_repository="")
    assert providernoimage["error"] == True
