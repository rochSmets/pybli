
This repo contains the def of 2 objects in order to manage bibtex refs :

`biblist` is a `list` of `dict` (one for each bibtex ref)
`keys` is a list of keywords

it is based on `bibtexparser` (which then need to be pip installed)

in order to be used in interactive mode from a python3 shell, you could use
a command such as `python3 -i $HOME/Hub/pybli/start.py`

You should also have 4 env var in your `bashrc` :
`PYBLIO_BIB` containing the dir where you have your bibfiles,
`PYBLIO_KEY` containing the dir where you have your keyfiles (containing
the lists of keywords),
`PYBLIO_AUT` containing the dir where you have all the pdf of the refs and
`PYBLIO_VIE` containing the path of the viewer to display the pdf

