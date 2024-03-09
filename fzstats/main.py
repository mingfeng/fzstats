import os
from dataclasses import dataclass
from typing import Literal, Annotated

import typer
from rich.console import Console
from rich.table import Table


@dataclass
class PathSize:
    name: str
    type: Literal["file", "folder"]
    size: int


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


def get_children_sizes(folder_path: str = ".") -> list[PathSize]:
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
    return children_with_sizes


def main(folder_path: Annotated[str, typer.Argument()] = "."):
    children_with_sizes = get_children_sizes(folder_path)
    table = Table("Name", "Type", "Size")
    for item in children_with_sizes:
        table.add_row(item.name, item.type, f"{item.size}B")
    
    console = Console()
    console.print(table)


if __name__ == "__main__":
    typer.run(main)
    
