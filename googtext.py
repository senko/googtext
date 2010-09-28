#!/usr/bin/env python
#
# googtext 0.1
# Written on 2009-03-27 by Senko Rasic <senko@senko.net>
# This software is Public Domain. Use it as you like.

import gtranslate
import polib
import sys

class GoogText:

    STRINGS_PER_REQUEST = 100

    def __init__(self, client_url, api_key=None):
        self.api = gtranslate.LanguageAPI(client_url, api_key)

    def translate(self, src_file, src_lang, dest_file, dest_lang):
        pofile = polib.pofile(src_file)

        entries = []
        ids = []

        for entry in pofile:
            entries.append(entry)

            # Sorry folks, this will get squashed
            txt = entry.msgid.replace('_', '')
            ids.append(txt)

            if len(ids) > self.STRINGS_PER_REQUEST:
                print len(ids), ids
                strs = self.api.translate_many(ids, src_lang, dest_lang)

                assert len(ids) == len(strs) == len(entries)

                for msg_str, e in zip(strs, entries):
                    e.msgstr = msg_str.strip()

                ids = []
                entries = []

        pofile.save(dest_file)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.stderr.write('Usage: %s <src.po> <src_lang> <dest.po> <dest_lang>\n' % sys.argv[0])
        sys.exit(-1)

    key = open('/home/senko/google-api-key.txt').read().strip()
    gt = GoogText('http://senko.net/services/googtext/', key)
    gt.translate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    sys.exit(0)


