# fzstats - File and Folder Size Statistics

fzstats is a Python command line tool that allows you to display statistics for file and folder sizes. Gain insights into the distribution of sizes within a directory, and easily sort and analyze the data.

## Installation

Install fzstats using pip:

```bash
pip install fzstats
```

## Usage

Show help message:

```bash
fzstats --help
```

Display size statistics for a folder, by default the results is sorted by size in descending order:

```bash
fzstats /path/to/your/folder
```

Sort the results by size in ascending order:

```bash
fzstats -s  /path/to/your/folder
```

Sort the results by name in descending order:

```bash
fzstats -s name /path/to/your/folder
```

Limit the results to 10 rows:

```bash
fzstats -l 10 /path/to/your/folder
```

## Options

* `--help`: Display help message.
* `-s`, `--sort`: Sort the results by a specific attribute. [default: size]
* `-d`, `--dir`: Sort direction. [default: desc]
* `-l`, `--limit`: Limit the results to a given number of rows. [default: no limit]
