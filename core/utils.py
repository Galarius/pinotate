# -*- coding: utf-8 -*-

import re 

# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))

def generate_md(title, highlights):
        text = '# {}\n\n'.format(title)
        for highlight in highlights:
            text += '> {}\n\n'.format(highlight)
        return text