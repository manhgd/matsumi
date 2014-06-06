import tornado.auth
from handler.base import Handler
import time

class Login(Handler):

    def log_success(self, user):
        self.set_secure_cookie('log_token', str(time.time()))
        self.session['user'] = user
        self.redirect(self.get_query_argument('next', '/'))

    def get(self):
        ''' Redirect to login page '''
        pass
        
class GoogleLogin(Login, tornado.auth.GoogleMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("openid.mode", None):
            # email, name, and locale
            user = yield self.get_authenticated_user()
            self.log_success(user)
        else:
            yield self.authenticate_redirect()
    
    def post(self):
        ''' Log out '''
        self.clear_all_cookies()
        self.redirect('/')
            
class Profile(Handler):
    def get(self):
        self.render("profile.html")
        
    def post(self):
        pass
        
    