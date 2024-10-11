from pathlib import Path
from typing import List, Literal

from coderag.logging import logger
from langchain_community.document_loaders.generic import Document, GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

LanguageType = Literal[
    "cpp",
    "go",
    "java",
    "kotlin",
    "js",
    "ts",
    "php",
    "proto",
    "python",
    "rst",
    "ruby",
    "rust",
    "scala",
    "swift",
    "markdown",
    "latex",
    "html",
    "sol",
    "csharp",
    "cobol",
    "c",
    "lua",
    "perl",
    "elixir",
]


class CodeBaseLoader:
    def __init__(self, path: str, language: LanguageType):
        self.path = Path(path)
        self.language = language

        if not language:
            raise ValueError("Language cannot be empty.")

        if language not in [
            "go",
            "python",
            "javascript",
            "typescript",
            "java",
            "c",
            "cpp",
            "rust",
            "ruby",
            "php",
        ]:
            raise ValueError(f"Unsupported language: {language}")

    def code_loader(self) -> List[Document]:
        if not self.path.exists():
            logger.error(f"Path {self.path.name} does not exist.")
            return []
        loader = GenericLoader.from_filesystem(
            self.path,
            glob="**/*",
            suffixes=[
                ".js",
                ".ts",
                ".go",
                ".py",
                ".java",
                ".c",
                ".cpp",
                ".h",
                ".hpp",
                ".rs",
                ".rb",
                ".php",
                ".html",
            ],
            exclude=[
                "Dockerfile",
                "vendor",
                "docker-compose.yml",
                "Makefile",
                "README.md",
                "build",
                "dist",
                "node_modules",
                "target",
                "out",
                ".git",
                ".idea",
                ".vscode",
                ".venv",
                ".pytest_cache",
                ".tox",
                ".mypy_cache",
                ".cache",
                ".eggs",
                ".ipynb_checkpoints",
                ".gitignore",
                ".dockerignore",
                ".gitattributes",
                ".editorconfig",
                ".pre-commit-config.yaml",
                ".flake8",
                ".pylintrc",
                ".gitlab-ci.yml",
                ".travis.yml",
                ".github",
                ".gitignore",
                ".gitattributes",
                ".editorconfig",
                ".pre-commit-config.yaml",
                ".flake8",
                ".pylintrc",
                ".gitlab-ci.yml",
                ".travis.yml",
                ".github",
            ],
            parser=LanguageParser(language=self.language, parser_threshold=1),
        )

        if not loader:
            logger.error("No loader found.")

        documents = loader.load()

        if not documents:
            logger.error("No documents found.")

        logger.info(f"Loaded {len(documents)} documents.")
        return documents
