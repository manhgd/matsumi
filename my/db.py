import sqlite3
import psycopg2
import psycopg2.extras


class Mixin:
    db = None
  
class DBAL:
    # Implemented abstract DB 
    
    def __init__(self, config):
        self.config = config
        self.connection = None
        
    def cursor(self, factory=None):
        if not self.connection:
            self.connect()
            
        if factory:
            return self.connection.cursor(cursor_factory=factory)
        else:
            return self.connection.cursor()
        
    def query_cursor(self):
        return self.cursor()
        
    def query(self, sql, args = ()):
        return self._query(sql, args, 'fetchall')
        
    def query_one(self, sql, args = ()):
        return self._query(sql, args, 'fetchone')
    
    def _query(self, sql, args = (), fetcher=None):
        ''' Generic '''
        cursor = self.query_cursor()
        cursor.execute(sql, args)
        if fetcher:
            return getattr(cursor, fetcher)()
        else:
            return cursor
            
    def insert(self, table, args):
        cursor = self.cursor()
        sql = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(
            table,
            ','.join(args.keys()),
            ', '.join(['%s' for x in range(len(args))])
        )
        self.execute(sql, tuple(args.values()))
        
    def execute(self, sql, args = ()):
        cursor = self.cursor()
        cursor.execute(sql, args)
        cursor.close()

class SQLite(DBAL):
    def connect():
        self.connection = sqlite3.connect(self.config)
        
class Postgres(DBAL):
    def query_cursor(self):
        return self.cursor(psycopg2.extras.DictCursor)
        
    def connect(self):
        self.connection = psycopg2.connect(**self.config)
        self.connection.autocommit = True
    
