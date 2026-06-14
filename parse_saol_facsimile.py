import ast
import json
import os
import re
import sys
import textwrap
from ast import Constant, Dict, Expr
from pathlib import Path
from typing import Any, NamedTuple

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class FacsimileEntry(NamedTuple):
    normaliserat_ord: str
    homonr: int
    ordkl: str
    stycke: str
    sidnr1: int
    sidnr2: int
    urspr_lopnr: int
    subnr: int
    text: str
    source: str
    upos: str
    ord: str


def word_dict_ast(entry: FacsimileEntry) -> Dict:
    return Dict(
        keys=[Constant(value="word"), Constant(value="upos"), Constant(value="conj")],
        values=[
            Constant(value=entry.normaliserat_ord),
            Constant(value=entry.upos),
            Constant(value=entry.text),
        ],
    )


def saol_entry_ast(entry: FacsimileEntry) -> Expr:
    tree = ast.parse("SaolEntry(word=A, upos=B, conj=C)")
    args = tree.body[0].value.keywords

    word_arg = next((k for k in args if k.arg == "word"), None)
    upos_arg = next((k for k in args if k.arg == "upos"), None)
    conj_arg = next((k for k in args if k.arg == "conj"), None)

    word_arg.value = Constant(entry.normaliserat_ord)
    upos_arg.value = Constant(entry.upos)
    conj_arg.value = Constant(entry.text)

    return tree


def write_wordlist_python_file(
    source_path: os.PathLike,
    destination_path: os.PathLike,
    license_notice: str,
) -> None:
    with open(source_path, "r") as i:
        entries = (FacsimileEntry(**json.loads(line)) for line in i.readlines())

    # ast.unparse() doesn't seem to produce multiline expressions,
    # so we split the list into lines manually
    words_ast = ast.parse(
        textwrap.dedent(
            f"""
            from saol.types import SaolEntry
            _license_notice = "{license_notice}"
            words = [LIST_CONTENTS_PLACEHOLDER]
            """
        )
    )
    output = ast.unparse(words_ast).replace(
        "LIST_CONTENTS_PLACEHOLDER",
        "".join([f"\n  {ast.unparse(saol_entry_ast(entry))}," for entry in entries])
        + "\n",
    )

    with open(destination_path, "w") as o:
        o.write(output + "\n")


class CustomBuildHook(BuildHookInterface):
    PLUGIN_NAME = "saol-parser"

    def initialize(self, version: str, build_data: dict[str, Any]):
        sys.path.insert(0, self.root)
        from download_saol_facsimile import add_artifact, read_wordlist_spec

        wordlists = read_wordlist_spec()

        if not wordlists:
            msg = "No wordlists provided"
            raise ValueError(msg)

        wordlists_dir = Path("src/saol/wordlist")
        wordlists_dir.mkdir(exist_ok=True)

        generated_files = []
        for wordlist in wordlists:
            input_file = Path("data", wordlist.filename)
            print(f"Processing {input_file}")

            name = re.match(r"(saol[^-]+)-faksimil.jsonl", input_file.name).group(1)
            destination_file = wordlists_dir / (f"{name}.py")

            write_wordlist_python_file(
                input_file, destination_file, wordlist.license_notice
            )
            add_artifact(build_data, self.root, destination_file)

            generated_files.append(name)

        init_file = wordlists_dir / "__init__.py"
        with open(init_file, "w") as initfile:
            for modulename in generated_files:
                initfile.write(f"from .{modulename} import words as {modulename}\n")
        build_data["artifacts"].append(str(init_file))
