from handler.base import Handler
import xml.etree.ElementTree

class Dict(Handler):
    def get(self, word):
        found = self.db.query_one('SELECT kanji, reading, sense FROM dict WHERE kanji = %s', (word + '%',))
        if not found:
            found = self.db.query_one('SELECT kanji, reading, sense FROM dict WHERE kanji LIKE %s ORDER BY LENGTH(kanji) ASC', (word + '%',))
            
        if found:
            if (self.get_query_argument('brief', False)):
                root = xml.etree.ElementTree.fromstring(found['sense'])
                sense = []
                for s in root.iter('sense'):
                    sense.append(s.find('gloss').text)
                self.write({'writing': found['kanji'].split(',')[0], 'reading': found['reading'], 'brief': ', '.join(sense)})
            else:
                self.set_header('Content-Type', 'text/plain')
                self.write({'dict': found})
        else:
            self.write({'error':'not found'})
            
class Example(Handler):
    def get(self, word):
        found = self.db.query('SELECT id, sentence, translation FROM example WHERE sentence LIKE %s  ORDER BY RANDOM() LIMIT 1', ('%' + word + '%',))
        if found:
            self.write({'example': found})
        else:
            self.write({'error':'not found'})