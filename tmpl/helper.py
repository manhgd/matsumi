import markdown
import markdown.extensions

def md(text):
    return markdown.markdown(text, extensions=[
        'nl2br', 'tables', 'sane_lists', 'fenced_code', 'attr_list', 'def_list'
    ])