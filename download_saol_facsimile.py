from pathlib import Path
from shutil import copyfileobj
from typing import Any, NamedTuple
from urllib.parse import urlparse
from urllib.request import urlopen

import tomllib
from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class WordlistDefinition(NamedTuple):
    url: str
    license_notice: str


def read_wordlists() -> list[WordlistDefinition]:
    with open("pyproject.toml", "rb") as f:
        return [
            WordlistDefinition(**entry)
            for entry in tomllib.load(f)["saol"]["wordlist"]
        ]


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "saol-downloader"

    def initialize(self, version: str, build_data: dict[str, Any]):
        wordlists = read_wordlists()

        data_dir = Path(self.root, "data")
        data_dir.mkdir(parents=True, exist_ok=True)

        for wordlist in wordlists:
            parsed_url = urlparse(wordlist.url)
            filename = Path(parsed_url.path).name

            wordlist_path = data_dir / filename
            license_path = wordlist_path.with_name(f"{filename}.license")

            with (
                urlopen(wordlist.url) as response,
                open(wordlist_path, "wb") as output_file,
            ):
                copyfileobj(response, output_file)

            with open(license_path, "w") as f:
                f.write(wordlist.license_notice)
