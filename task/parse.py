from dbal import DBAL
import xml.etree.ElementTree
import re

import config

class JapaneseDataParser:
    
    db = None
    COMMIT_INTERVAL = 500

    def __init__(self):
        self.db = DBAL({
            'adapter': 'postgres',
            'dsn': config.dsn
        })
        self.db.connection.autocommit = False
    
    def flatten(self, tree, xpath, sep=', '):
        return sep.join([x.text for x in tree.findall(xpath)])
        
    def jmdict(self):
        tree = xml.etree.ElementTree.ElementTree()
        tree.parse(config.path + '/doc/jmdict.dat')
        k = 0
        for entry in tree.getroot():
            sense = []
            for s in entry.findall('sense'):
                sense.append(xml.etree.ElementTree.tostring(s).decode('utf-8'))
            
            self.db.insert('dict', dict(
                ent_seq = entry.find('ent_seq').text,
                kanji = self.flatten(entry, ".//keb"),
                reading = self.flatten(entry, ".//reb"),
                sense = "<ul><li>" + ("</li><li>".join(sense)) + "</li></ul>"
            ))
            k += 1
            if k % self.COMMIT_INTERVAL:
                self.db.connection.commit()
        self.db.connection.commit()
        
    def example(self):
        match_regex = re.compile('^A:(.+)\t(.+)#')
        k = 0
        with open(config.path + '/doc/example.dat') as f:
            for line in f:
                matched = match_regex.match(line)
                if not matched:
                    continue
                self.db.insert('example', dict(
                    sentence=matched.group(1), translation=matched.group(2)
                ))
                k += 1
            if k % self.COMMIT_INTERVAL:
                self.db.connection.commit()
        self.db.connection.commit()

def execute():
    parser = JapaneseDataParser()
    parser.example()
    parser.jmdict()
