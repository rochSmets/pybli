
from bibtexparser import load
from bibtexparser import loads
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

import glob
import os
import string
import tempfile
import subprocess



class biblist(list):

    def __init__(self, bibfile=-1):

        """
        object to manage a list of bibtex refs : each ref is a dictionnary

        """

        if bibfile == -1:
            initlist = []
            for fil in glob.glob("*.bib"):
                with open(fil) as bf:
                    bl = load(bf)
                    initlist.extend(bl.entries)

            self.name = 'all.bib'
            super(biblist, self).__init__(initlist)


        elif bibfile == '':
            self.name = 'empty.bib'
            super(biblist, self).__init__()

        elif type(bibfile) is str:
            with open(bibfile) as bf:
                bl = load(bf)

            self.name = bibfile
            super(biblist, self).__init__(bl.entries)

        else:
            raise NameError('bad bibfile name')


    def list(self):

        """
        print the list of `ID`s of the biblist with their index

        """

        print('')
        for index in range(len(self)):
            print('{0:24}  : {1:3}'.format(self[index]['ID'], index))
        print('')


    def show(self, identry):

        """
        display the main fields of an entry (either an int or the 'ID' string)

        """

        if type(identry) == str:
            for item in self:
                if item['ID'] == identry:
                    dic = item
                    index = self.index(item)

        elif type(identry) == int:
            dic = self[identry]
            index = identry

        else:
            raise TypeError('ID entry has to be a \'str\' (the bibcode) or a\
                             \'int\' (the index of the entry in the biblist)')

        print('')
        print('ID                        : {0}'.format(dic['ID']))
        print('index                     : {0}'.format(index))
        print('author                    : {0}'.format(dic['author']))
        print('title                     : {0}'.format(dic['title']))
        print('year                      : {0}'.format(dic['year']))
        print('type                      : {0}'.format(dic['ENTRYTYPE']))
        print('keyword                   : {0}'.format(dic['keyword']))

        notes = dic['note'].split("\n")
        for note in notes:
            print('note                      : {0}'.format(note))

        if dic['ENTRYTYPE'] == 'article' :
            print('journal                   : {0}'.format(dic['journal']))
        print('')


    def clean(self):

        """
        do several add/substitution in the biblist :
            - remove the `adsnote`, 'eprint', 'archiveprefix', 'primaryclass',
              'eid' and 'file' entries
            - put 'TBD' for 'keyword' if empty or not existing
            - put 'None' for 'note' if empty or not existing
            - make sure mandatory fields are in the biblist (only for article)

        """

        print('')
        for i in range(len(self)):
            if 'adsnote' in self[i]:
                self[i].pop('adsnote')
                print('{0:24}  : remove \'adsnote\''.format(self[i]['ID']))

            if 'keywords' in self[i]:
                self[i].pop('keywords')
                print('{0:24}  : remove \'keywords\''.format(self[i]['ID']))

            if 'eprint' in self[i]:
                self[i].pop('eprint')
                print('{0:24}  : remove \'eprint\''.format(self[i]['ID']))

            if 'archiveprefix' in self[i]:
                self[i].pop('archiveprefix')
                print('{0:24}  : remove \'archiveprefix\''.format(self[i]['ID']))

            if 'primaryclass' in self[i]:
                self[i].pop('primaryclass')
                print('{0:24}  : remove \'primaryclass\''.format(self[i]['ID']))

            if 'eid' in self[i]:
                self[i].pop('eid')
                print('{0:24}  : remove \'eid\''.format(self[i]['ID']))

            if 'file' in self[i]:
                self[i].pop('file')
                print('{0:24}  : remove \'file\''.format(self[i]['ID']))

            if 'keyword' in self[i]:
                if 'TBD' in self[i]['keyword']:
                    self[i]['keyword'] = 'TBD'
            else:
                self[i].update({str('keyword'): str('TBD')})
                print('{0:24}  : set \'TBD\' for \'keyword\''.format(self[i]['ID']))

            if 'note' in self[i]:
                pass
            else:
                self[i].update({str('note'): str('None')})
                print('{0:24}  : set \'None\' for \'note\''.format(self[i]['ID']))

        articleList = ['ID', 'author', 'journal', 'month', 'pages', 'title', 'volume', 'year']

        for i in range(len(self)):
            entry = self[i]
            if entry['ENTRYTYPE'] == 'article' :
                for k in articleList:
                    if k not in entry:
                        print('{0:24}  : has not key \'{1:8}\''.format(entry['ID'], k))

        self.autoyear()
        self.autokey()
        #self.autofile()
        print('')


    def display(self, identry):

        """
        call mupdf for the entry (either an int or the 'ID' string)

        """

        if type(identry) == str:
            base = identry

        elif type(identry) == int:
            base = self[identry]['ID']
            identry = base

        else:
            raise TypeError('ID entry has to be a \'str\' (the bibcode) or a\
                             \'int\' (the index of the entry in the biblist)')

        # base contains the name of the author
        for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+']:
            base = base.replace(i, "")
        filename = os.path.join(os.path.expandvars('$PYBLIO_AUT'), base, identry+'.pdf')

        #os.system('mupdf '+filename+' &')
        os.system(os.path.expandvars('$PYBLIO_VIE')+' '+filename+' &')


    def save(self, bibfile=-1):

        """
        save the biblist with :
            - the original filename without any arg
              or
            - the given file name if not empty

        """

        if bibfile == -1:
            bibfile = self.name

        db = BibDatabase()
        for item in self:
            db.entries.append(item)

        writer = BibTexWriter()    # this class is needed to prepare format
        writer.indent = '   '      # indent entries with 4 spaces instead of one
        writer.comma_first = False # place the comma at the beginning of the line
        writer.align_values = True # with a nice indentation

        print('')
        print(os.path.join(os.path.expandvars('$PYBLIO_BIB'), bibfile))
        print('')

        with open(os.path.join(os.path.expandvars('$PYBLIO_BIB'), bibfile), 'w') as bf:
            bf.write('\n')
            bf.write(writer.write(db))
            bf.write('\n')


    def addkey(self, identry, keylist=-1):

        """
        this method is intended to add keywords by calling the pick method
        of the 'all' keys object
        if existing, former keywords are added by default

        """


        from keys import keys

        if keylist == -1:
            ak = keys()
        else:
            raise NotImplementedError('keylist != -1 not yet implemented')

        if type(identry) == int:
            out = ak.pick(self[identry]['keyword'])

        elif type(identry) == str:
            for item in self:
                if item['ID'] == identry:
                    dic = item
                    index = self.index(item)
                    out = ak.pick(self[index]['keyword'])

        arg = ''

        for item in out:
            if arg != '':
                arg = arg + ', '
            arg = arg + item

        self.set(identry, 'keyword', arg)
        self.show(identry)


    def addnotes(self, identry):

        """
        call a vim editor in order to edit existing notes
        or add new one

        """

        if type(identry) == int:
            index = identry

        elif type(identry) == str:
            for item in self:
                if item['ID'] == identry:
                    dic = item
                    index = self.index(item)

        out = self[index]['note']
        if out == 'None' :
            out = ''

        arg = out.encode('utf-8')

        EDITOR = os.environ.get('EDITOR','vim')

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:

            tf.write(arg)
            tf.flush()

            subprocess.call([EDITOR, tf.name])

            tf.seek(0)
            notes = tf.read()

            self.set(identry, 'note', notes.decode("utf-8"))
            self.show(identry)


    def find(self, fields, args):

        """
        find all entries which 'fields' equals 'args':
            - 'fields' and 'args' need to have the same length
              (whatever list or tuple)
            - they can also be a single string
        all the 'args' of 'fields' has to be in the ref to pick this one...
        except for 'author', for which at least one of the given author
        has to be in the ref to pick it

        """

        from keys import keys

        if type(fields) is str:
            fields = list({fields})

        if type(args) is str:
            args = list({args})

        if len(fields) != len(args):
            raise ValueError("fields and args have to be lists of same length")

        items = []
        for ref in range(len(self)):

            found = False
            for i in range(len(fields)):


                if fields[i] == 'keyword':
                    if args[i] == '':
                        ak = keys()
                        args[i] = ak.pick()

                if type(args[i]) == str:
                    args[i] = list({args[i]})

                if fields[i] == 'author':
                    for arg in args[i]:
                        if arg.lower() in self[ref]['author'].lower():
                            found = True

                else:
                    for arg in args[i]:
                        if arg.lower() in self[ref][fields[i]].lower():
                            found = True

            if found is True:
                items.append(ref)

        print('')
        for ref in items:
                print('{0:24}  : {1:3}'.format(self[ref]['ID'], ref))
        print('')


    def autoyear(self):

        """
        be sure the year in 'ID' equals the year recorded in biblist

        """

        for i in range(len(self)):
            identry = self[i]['ID']

            out = [s for s in identry if s.isdigit()]
            year = ''.join(out)

            if year != self[i]['year']:
                print('year might be wrong       : {0}'.format(identry))


    def autokey(self):

        """
        be sure keywords are separated by commas

        """

        for i in range(len(self)):
            entry = self[i]
            if 'keyword' in entry:
                keyword = entry['keyword'].replace(';', ',')
                entry.update({str('keyword'): str(keyword)})


    def nokey(self):

        """
        display the entries w/o keyword

        """

        items = []
        for ref in range(len(self)):
            if self[ref]['keyword'] == 'TBD':
                items.append(ref)

        print('')
        for ref in items:
                print('{0:24}  : no keyword ({1:3})'.format(self[ref]['ID'], ref))
        print('')


    def nonotes(self):

        """
        display the entries w/o note

        """

        items = []
        for ref in range(len(self)):
            if self[ref]['note'] == 'None':
                items.append(ref)

        print('')
        for ref in items:
                print('{0:24}  : no note ({1:3})'.format(self[ref]['ID'], ref))
        print('')


    def set(self, identry, field, arg):

        """
        set 'arg' in the 'field' of 'identry'
        not directly called, but needed in addnotes and addkeys

        """

        if type(identry) == str:
            for i in range(len(self)):
                if self[i]['ID'] == identry:
                    self[i].update({str(field): str(arg)})

        elif type(identry) == int:
            self[identry].update({str(field): str(arg)})


        else:
            raise TypeError('ID entry has to be a \'str\' (the bibcode) or a\
                             \'int\' (the index of the entry in the biblist)')


    #def autofile(self):

    #    """
    #    set the full filename for the associated pdf
    #    TODO : might be removed in close future

    #    """

    #    toremove = list(string.ascii_lowercase)+['+', '.']

    #    for ref in range(len(self)):

    #        name = self[ref]['ID']

    #        for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+']:
    #            name = name.replace(i, "")
    #        filename = os.path.join(os.path.expandvars('$PYBLIO_AUT'), name, self[ref]['ID']+'.pdf')

    #        self[ref].update({str('file'): str(filename)})
    #        print('{0:24}  : set file to {1}'.format(self[ref]['ID'], filename))


    #def entry(self, identry):

    #    """
    #    return the dict of the (mandatory) entry (which is the 'ID' string)
    #    TODO : might be removed in close future

    #    """

    #    if type(identry) is str:
    #        for item in self:
    #            if item['ID'] == identry:
    #                return item
    #    else:
    #       raise TypeError('ID must be a str')


    #def add(self, identry, field, arg):

    #    """
    #    add 'arg' in the 'field' of 'identry'
    #    TODO : might be removed in close future

    #    """

    #    if type(identry) == str:
    #        for i in range(len(self)):
    #            if self[i]['ID'] == identry:
    #                oldarg = self[i][field]
    #                newarg = oldarg + str(', '+arg)
    #                self[i].update({str(field): str(newarg)})

    #    elif type(identry) == int:
    #        oldarg = self[identry][field]
    #        newarg = oldarg + str(', '+arg)
    #        self[identry].update({str(field): str(newarg)})
    #        self[identry].update({str(field): str(arg)})

    #    else:
    #        raise TypeError('ID entry has to be a \'str\' (the bibcode) or a\
    #                         \'int\' (the index of the entry in the biblist)')


    #def join(self, entrystring):

    #    """
    #    join an entry (of string type) at the end of the biblist
    #    TODO : might be removed in close future

    #    """


    #    entrystring = entrystring.replace('month = jan', 'month = {jan}')
    #    entrystring = entrystring.replace('month = fev', 'month = {fev}')
    #    entrystring = entrystring.replace('month = mar', 'month = {mar}')
    #    entrystring = entrystring.replace('month = apr', 'month = {apr}')
    #    entrystring = entrystring.replace('month = may', 'month = {may}')
    #    entrystring = entrystring.replace('month = jun', 'month = {jun}')
    #    entrystring = entrystring.replace('month = jul', 'month = {jul}')
    #    entrystring = entrystring.replace('month = aug', 'month = {aug}')
    #    entrystring = entrystring.replace('month = sep', 'month = {sep}')
    #    entrystring = entrystring.replace('month = oct', 'month = {oct}')
    #    entrystring = entrystring.replace('month = nov', 'month = {nov}')
    #    entrystring = entrystring.replace('month = dec', 'month = {dec}')

    #    bt = loads(entrystring)
    #    self.append(bt.entries[0])

    #    if 'keyword' in bt.entries[0]:
    #        pass
    #    else:
    #        bt.entries[0].update({str('keyword'): str('TBD')})

    #    if 'note' in bt.entries[0]:
    #        pass
    #    else:
    #        bt.entries[0].update({str('note'): str('None')})

