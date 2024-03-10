import os
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Literal

import typer
from rich.console import Console
from rich.table import Column, Table


@dataclass
class PathSize:
    name: str
    type: Literal["file", "folder"]
    size: int


class SortBy(Enum):
    NAME = "name"
    TYPE = "type"
    SIZE = "size"


def get_folder_size(folder_path="."):
    """Get folder size

    Args:
        folder_path (str, optional): path to the folder. Defaults to '.'.

    Returns:
        int: folder size in bytes
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def get_children_sizes(
    folder_path: str = ".",
    sort_by: str = "size",
) -> list[PathSize]:
    """Get folder children and their sizes

    Args:
        folder_path (str, optional): Path to the folder. Defaults to ".".

    Returns:
        list[PathSize]: children with the their sizes
    """
    children_with_sizes = []
    for child in os.listdir(folder_path):
        child_path = os.path.join(folder_path, child)

        if os.path.isfile(child_path):
            size = os.path.getsize(child_path)
            children_with_sizes.append(PathSize(child, "file", size))
        elif os.path.isdir(child_path):
            size = get_folder_size(child_path)
            children_with_sizes.append(PathSize(child, "folder", size))
    # by default sort results by size in descending order
    children_with_sizes.sort(key=lambda item: getattr(item, sort_by), reverse=True)
    return children_with_sizes


def format_size(size: int) -> str:
    one_kb = 1024
    one_mb = 1024**2
    one_gb = 1024**3
    if size > one_gb:
        return f"{size / one_gb:.1f}G"
    if size > one_mb:
        return f"{size / one_mb:.1f}M"
    if size > one_kb:
        return f"{size / one_kb:.1f}K"
    return f"{size}B"


def main(
    folder_path: Annotated[str, typer.Argument()] = ".",
    sort_by: Annotated[SortBy, typer.Option("--sort", "-s")] = "size",
):
    children_with_sizes = get_children_sizes(folder_path, sort_by.value)
    table = Table(
        "Name",
        Column("Size", justify="right", style="green"),
    )
    for item in children_with_sizes:
        name = item.name if item.type == "file" else f"[blue]{item.name}"
        table.add_row(name, format_size(item.size))

    console = Console()
    console.print(table)


if __name__ == "__main__":
    typer.run(main)
