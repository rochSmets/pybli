
This repo contains the def of 2 objects in order to manage bibtex refs :

`biblist` is a `list` of `dict` (one for each bibtex ref)
`keys` is a list of keywords

it is based on `bibtexparser`
in a dedicated virtualenv (recommended) :
```
pip install bibtexparser
```

in order to be used in interactive mode from a python3 shell, you could use
a command such as `python3 -i $HOME/Hub/pybli/start.py`

You should also have 4 env var in your `bashrc` :
`PYBLIO_BIB` dir where the bibfiles are,
`PYBLIO_KEY` dir where the keyfiles are (files with the lists of keywords),
`PYBLIO_AUT` dir where you have the pdf (below the author dir name)
`PYBLIO_VIE` path of the viewer to display the pdf

