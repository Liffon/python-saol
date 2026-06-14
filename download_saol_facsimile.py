import os
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
    filename: str


def read_wordlist_spec() -> list[WordlistDefinition]:
    def filename(url):
        parsed_url = urlparse(url)
        return Path(parsed_url.path).name

    with open("pyproject.toml", "rb") as f:
        return [
            WordlistDefinition(filename=filename(entry["url"]), **entry)
            for entry in tomllib.load(f)["saol"]["wordlist"]
        ]


def add_artifact(build_data: dict[str, Any], root: os.PathLike, artifact: Path) -> None:
    if artifact.is_relative_to(root):
        artifact = artifact.relative_to(root)

    print(f"Adding artifact {artifact}")
    build_data["artifacts"].append(str(artifact))


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "saol-downloader"

    def initialize(self, version: str, build_data: dict[str, Any]):
        wordlists = read_wordlist_spec()

        if not wordlists:
            msg = "No wordlists provided"
            raise ValueError(msg)

        data_dir = Path(self.root, "data")
        data_dir.mkdir(parents=True, exist_ok=True)

        for wordlist in wordlists:
            filename = wordlist.filename

            wordlist_path = data_dir / filename

            if not wordlist_path.exists():
                print(f"Downloading {wordlist.url}")
                with (
                    urlopen(wordlist.url) as response,
                    open(wordlist_path, "wb") as output_file,
                ):
                    copyfileobj(response, output_file)
            add_artifact(build_data, self.root, wordlist_path)
