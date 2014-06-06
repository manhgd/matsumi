import tornado.web
import tornado.util
import my.db
import my.session

class Handler(tornado.web.RequestHandler, my.db.Mixin, my.session.Mixin):

    def initialize(self):
        self.db = my.db.Postgres(self.application.config.database)
        self.session = None
        self.session_prepare()
        
    def set_default_headers(self):
        # For security
        self.clear_header('Server')
    
    def get_current_user(self):
        log_token = self.get_secure_cookie('log_token', None)
        if log_token:
            return self.session['user']['name']
        else:
            return None
    
    def get_cookie_utf8(self, name):
        value = self.get_secure_cookie(name)
        if value:
            return value.decode('utf-8')
        
    def write_error(self, status_code, **kwargs):
        if self.settings['debug']:
            super().write_error(status_code, **kwargs)
        else:
            self.render('error', code=status_code)
    def bulk_arguments(self, fields):
        return { field: self.get_body_argument(field, '') for field in fields }
        
    def get_template_namespace(self):
        namespace = super().get_template_namespace()
        namespace.update({
            'helper': tornado.util.import_object('tmpl.helper')
        })
        return namespace