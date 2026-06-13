from pathlib import Path
from shutil import copyfileobj
from typing import Any
from urllib.parse import urlparse
from urllib.request import urlopen

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "saol-downloader"

    def initialize(self, version: str, build_data: dict[str, Any]):
        data_dir = Path(self.root, "data")
        data_dir.mkdir(parents=True, exist_ok=True)

        for url in self.config["urls"]:
            parsed_url = urlparse(url)
            filename = Path(parsed_url.path).name

            with urlopen(url) as response, open(data_dir / filename, "wb") as output_file:
                copyfileobj(response, output_file)
