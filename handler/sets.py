from handler.base import Handler
import tornado.web
import re

class Set(Handler):
    @tornado.web.authenticated
    def get(self, action):
        if action == 'new':
            self.render('set_new.html')
        else:
            self.render('set_list.html', avail = self.db.query('SELECT id, name, words FROM sets'))    
    
    @tornado.web.authenticated
    def post(self, action):
        self.check_xsrf_cookie()
        data = self.bulk_arguments(('name', 'words',))
        data['owner'] = self.session['user']['email']
        self.db.insert('sets', data)
        self.redirect('/sets/list')
        
class SetMixin():
    def set_record(self, set_id):
        the_set = self.db.query_one('SELECT * FROM sets WHERE id = %s', (set_id,))
        return dict(
            the_set = the_set,
            words_list = re.split('\s+', the_set['words'])
        )
    
class Words(Handler, SetMixin):
    def get(self, set_id = None):
        if not set_id:
            self.redirect('/sets/list')
            return
        self.render('dict.html', **(self.set_record(set_id)))
    
class Example(Handler, SetMixin):
    def get(self, set_id = None):
        if not set_id:
            self.redirect('/sets/list')
            return
        self.render('example.html', **(self.set_record(set_id)))
