
#import theme
import glob
import os
import tempfile
import subprocess



class keys(dict):

    def __init__(self, entry=-1):

        """
        objects of class "keys" are intended to manage the keywords :
            - keyFilesList is the list containing the key files
            - keyList is the list of all keywords in a given key file
            - dicKey is the associated dictionary

        """

        # default key dictionnary, containing the keywords of all key files
        if entry == -1:
            keyFiles = os.path.join(os.path.expandvars('$PYBLIO_KEY'), '*.key')
            keyFilesList = []
            for fil in glob.glob(keyFiles):
                keyFilesList.append(fil)

            keyList = []
            dicKey = {}

            for keyfile in keyFilesList:
                f = open(keyfile, 'r')
                itemlist = f.read().splitlines()
                f.close()
                for item in itemlist:
                    if item != '':
                        keyList.append(item)

            for i in range(len(keyList)):
                dicKey[keyList[i]] = i

            self.name = 'all.key'

            super(keys, self).__init__(dicKey)

        # empty key dictionnary
        elif entry == '':
            self.name = 'empty.key'

            super(keys, self).__init__()

        # key dictionnary for a given key file
        elif os.path.isfile(os.path.join(os.path.expandvars('$PYBLIO_KEY'), entry)):
            name = entry
            entry = os.path.join(os.path.expandvars('$PYBLIO_KEY'), entry)
            keyList = []
            dicKey = {}

            f = open(entry, 'r')
            itemlist = f.read().splitlines()
            f.close()
            for item in itemlist:
                if item != '':
                    keyList.append(item)

            for i in range(len(keyList)):
                dicKey[keyList[i]] = i

            self.name = name

            super(keys, self).__init__(dicKey)

        else:
           raise NameError('bad keyfile name')

        self.keyList = keyList


    def list(self):

        """
        print the list of keywords, ordered by values

        """

        print('')
        for item in sorted(dict(self), key=lambda x: x[0].lower()):
            print('{0:24}  : {1:3}'.format(item, self[item]))
        print('')


    def pick(self, old=-1):

        """
        pick keywords in the keyList of the object and return a list
        the keywords are listed in a file edited with vim...
        if keywords are already existing, they are marked so in the file

        """

        EDITOR = os.environ.get('EDITOR','vim')

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:

            tf.write(b'')
            tf.flush()

            for key in self.keyList:
                if old == -1:
                    buff = '[ ] {0}\n'.format(key)
                elif type(old) is str:
                    if key in old:
                        buff = '[x] {0}\n'.format(key)
                    else:
                        buff = '[ ] {0}\n'.format(key)
                tf.write(buff.encode('utf-8'))

            tf.flush()

            subprocess.call([EDITOR, tf.name])

            tf.seek(0)
            all_keys = tf.read().splitlines()

            out = []

            for line in all_keys:
                string = line.decode("utf-8")
                if string[:3] != '[ ]':
                    out.append(string.split()[1])

            return out

