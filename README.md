# A Citation and Text-Based Framework for Retrieving Publications for Literature Reviews

This repository contains the Python implementation of a citation- and text-based framework for retrieving relevant publications for literature reviews, as described in:

Sarol, M. J., Liu, L., & Schneider, J. (2018). Testing a Citation and Text-Based Framework for Retrieving Publications for Literature Reviews. Proceedings of the 7th International Workshop on Bibliometric-enhanced Information Retrieval (BIR 2018), 22-33.

Paper: https://ceur-ws.org/Vol-2080/paper3.pdf

## Requirements
1. Python version 2.x
2. Scopus API (with permission to collect citation information)

## Usage

1. Open run.py and modify the following variables:

    review = scopus_id_of_review_file
    studies_folder = /path/to/folder/containing/included/studies
    output_folder = /path/to/output/folder

2. Add the required Scopus API credentials
3. Execute the script: `python2 run.py`

# BibTex Citation

```
@inproceedings{SarolLS18,
  author    = {Maria Janina Sarol and
               Linxi Liu and
               Jodi Schneider},
  title     = {Testing a Citation and Text-Based Framework for Retrieving Publications for Literature Reviews},
  booktitle = {Proceedings of the 7th International Workshop on Bibliometric-enhanced
               Information Retrieval},
  pages     = {22--33},
  year      = {2018},
  url       = {http://ceur-ws.org/Vol-2080/paper3.pdf}
}
```

# License

This project is licensed under the MIT License. See the LICENSE file for details. The license applies to the source code in this repository. Data obtained through the Scopus API may be subject to separate terms and restrictions.
