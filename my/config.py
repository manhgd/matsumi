import os
import os.path

path = os.path.dirname(os.path.dirname(__file__) + '/../')
host = '127.0.0.1'
port = 7654

timezone = 'Asia/Tokyo'
setting = dict(
    template_path=os.path.join(path, 'tmpl'),
    cookie_secret='TO_BE_FILLED',
    xsrf_cookies=False,
    login_url='',
    debug = True,
    static_path = os.path.join(path, 'static'),
)
routes = [
    # URL ("pattern", "module.Handler")
    (r"/(home|about)?",     'misc@Page'),
    (r"/sets/(new|list)",   'sets@Set'),
    (r"/words/(\d*)",       'sets@Words'),
    (r"/example/(\d*)",     'sets@Example'),
    (r"/api/dict/(.*)",     'api@Dict'),
    (r"/api/example/(.*)",  'api@Example'),
    (r"/gloss",             'misc@Gloss'),
    (r"/user/login",        'user@GoogleLogin'),
    (r"/user/logout",       'user@GoogleLogin'),
    (r"/user/profile",      'user@Profile'),
]

# Local
setting['login_url'] = '/user/login'
port = 7040
database = dict(database="matsumi", user="matsumi", password="")
setting.update(dict(
    cookie_secret = 'TO_BE_FILLED',
))
data_path = os.path.join(path , 'var')

# Deploy
if os.environ.get('OPENSHIFT_APP_NAME', False):
    setting.update(dict(
        debug = False,
        cookie_secret = 'TO_BE_FILLED',
    ))
    port = os.environ['OPENSHIFT_PYTHON_PORT']
    host = os.environ['OPENSHIFT_PYTHON_IP']
    database = dict(
        database=os.environ['PGDATABASE'],
        user=os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
        password=os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
        host=os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        port=os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']
    )
    data_path = os.environ['OPENSHIFT_DATA_DIR']
