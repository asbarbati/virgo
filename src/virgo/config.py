class Config:
    def __init__(self) -> None:
        """Configuration class for the Virgo Object.

        Args:
            None

        Returns:
            None
        """
        self.name = None
        self.image_repository = None
        self.git_ssh_url = None
        self.git_ssh_privatekey = None
        self.git_values_filename = None
        self.values_key = None

    def load(self, config: dict) -> None:
        """Load the config given from the file and inject it into the class vars.

        Args:
            config (dict): The config dict given from virgo.loader.Loader.read_config

        Returns:
            None
        """
        mandatory_vars = [
            "name",
            "image_repository",
            "git_ssh_url",
            "git_ssh_privatekey",
            "git_values_filename",
            "values_key",
        ]

        for itervar in mandatory_vars:
            if config[itervar]:
                setattr(self, itervar, config[itervar])
