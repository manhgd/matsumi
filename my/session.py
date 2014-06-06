import uuid
import pickle
import os.path

class Session:

    def __init__(self, meta):
        self.meta = meta
        self.data = None
    
    def __getitem__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None
    
    def __setitem__(self, name, val):
        self.data[name] = val
        self.save()
        
    def __len__(self):
        return len(self.data)
        
    def prepare(self):
        if not self.meta['id']:
            self.meta['is_fresh'] = True
            self.meta['id'] = self.generate_id()
            self.data = dict()
        else:
            # Exisiting session
            self.meta['is_fresh'] = False
            self.load()
        
    def save(self):
        ''' Abstract: save session data with session.id as the identiy '''
        pass
        
    def load(self):
        ''' Load the session data to session.data variable '''
        pass
    
    def generate_id(self):
        return uuid.uuid1().bytes
        return id
        
class FileSession(Session):

    def prepare(self):
        super().prepare()
        
    def file_path(self):
        name = 'sess_' + ''.join('{:02x}'.format(x) for x in self.meta['id'])
        return os.path.join(self.meta['save_path'], name)
        
    def save(self):
        with open(self.file_path(), 'w+b') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            
    def load(self):
        path = self.file_path()
        if not os.path.isfile(path):
            self.data = dict() 
        else:
            with open(path, 'rb') as f:
                self.data = pickle.load(f)
        
class Mixin:
        
    def session_prepare(self, config=None):
        if self.session:
            # Was ready, exit
            return
        meta = {
            'cookie_name': 'SESS',
            'storage': FileSession,
            'save_path': self.application.config.data_path,
            'request_ip': self.request.remote_ip,
        }
        if config:
            meta.update(config)
        meta['id'] = self.get_secure_cookie(meta['cookie_name'], None)
        self.session = meta['storage'](meta) # Instanate storage class
        self.session.prepare()
        if meta['is_fresh']:
            self.set_secure_cookie(meta['cookie_name'], self.session.meta['id'])
            
    def session_regenerate(self):
        pass