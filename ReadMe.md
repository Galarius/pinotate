Pinotate
========

> Export iBooks highlights

```
usage: pinotate.py [-h] [-o OUT] [-l] [--headings] [-s] [title]

Export iBooks highlights

positional arguments:
  title              export highlights of the book with specific title (optional)

optional arguments:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  output directory
  -l, --list         print books titles
  --headings         add headings to markdown
  -s, --sort         sort by location instead of time

Run `pinotate.py` to export all highlights to the current directory
```
Requirements:

* Python3

## Pinotate GUI

Requirements:

* [wxPython](https://wxpython.org/download.php#osx)
* [markdown](https://pypi.org/project/Markdown/)

LICENSE
=======

This project is licensed under the terms of the MIT license. (see LICENSE.txt in the root)  
