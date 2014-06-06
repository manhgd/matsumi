#!/usr/bin/env python3
import optparse
import task
import tornado.util
from clint.textui import puts, colored

def main():
    p = optparse.OptionParser()
    options, arguments = p.parse_args()
    try:
        cmd = tornado.util.import_object('task.' + arguments[0])
        return cmd.execute(options, arguments)
    except ImportError:
        puts(colored.red('Command not found'))
    except IndexError:
        puts(colored.yellow('Missing command argument'))
        print('Available command: ')
        print(task.available())
  
if __name__ == '__main__':
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)