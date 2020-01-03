
import os
import sys
import glob

bib = os.path.expandvars('$PYBLIO_BIB')
key = os.path.expandvars('$PYBLIO_KEY')

from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

from theme import *
from keys import *
from biblist import *


cwd = os.getcwd()

os.chdir(bib)
bibFiles = os.path.join('*.bib')
bibFilesList = []
for f in glob.glob(bibFiles):
    bibFilesList.append(f)

os.chdir(key)
keyFiles = os.path.join('*.key')
keyFilesList = []
for k in glob.glob(keyFiles):
    keyFilesList.append(k)

print('')
print('2 objects in \"pybli\" :')
print('')
print('- \"biblist\" to manage a \"list\" of bib (of type \"dict\")')
print('- \"keys\"    to manage the keywords    (of type \"dict\")')
print('')

os.chdir(key)
print('# __ key files loaded __')
for item in keyFilesList:
    print('{0:24}  :  {1:2}'.format(item, item[0:3]))
    vars()[item[0:3]] = keys(item)
alk = keys()
print('{0:24}  :  {1:3}'.format('all.key', 'alk'))
print('')

os.chdir(bib)
print('# __ bib files loaded __')
for item in bibFilesList:
    print('{0:24}  :  {1:3}'.format(item, item[0:3]))
    vars()[item[0:3]] = biblist(item)
alb = biblist()
print('{0:24}  :  {1:3}'.format('all.bib', 'alb'))
print('')

os.chdir(cwd)
