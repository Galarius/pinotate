# Pinotate

Pinotate is a Python-based tool designed to export highlights from iBooks. It offers both a command-line interface and a GUI version for user flexibility.

## Features
- **Export highlights**: Ability to export all highlights per book.
- **Export highlights of a specified book**: Ability to export highlights of a book with a specific title.
- **List books**: Display all book titles.
- **Markdown headings**: Add headings to the markdown export.
- **Sort options**: Sort the highlights either by location or by time.

## Usage

To use Pinotate, run the following command:

```
usage: pinotate.py [-h] [-o OUT] [-l] [--headings] [-s] [title]
```

- **Positional Argument**:
  - `title`: Export highlights of the book with a specific title (optional).
  
- **Optional Arguments**:
  - `-h, --help`: Show the help message and exit.
  - `-o OUT, --out OUT`: Specify the output directory.
  - `-l, --list`: Print book titles.
  - `--headings`: Add headings to markdown.
  - `-s, --sort`: Sort by location instead of time.

To export all highlights to the current directory, simply run:

```
pinotate.py
```

### Requirements

- Python 3

## Pinotate GUI

For those who prefer a graphical interface, Pinotate also offers a GUI version.

### Setup and Run

```shell
python3 -m venv .pyenv
source .pyenv/bin/activate
pip install -r requirements.txt
./pinotate-gui.py
```

### Requirements for GUI

- Python 3
- [wxPython](https://wxpython.org/download.php#osx)
- [markdown](https://pypi.org/project/Markdown/)

## License

This project is licensed under the terms of the MIT license. You can find the full license in the `LICENSE.txt` file located in the root directory.
