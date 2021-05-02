# -*- coding: utf-8 -*-

import re 

# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))

def generate_md(title, highlights, with_headings=True, normal_sorting=True):
    text = '# {}\n\n'.format(title)    
    if normal_sorting:
        highlights = sorted(highlights, key=(lambda highlight: (highlight.chapter, highlight.ref_in_chapter, highlight.created)), reverse=False)
    added_headings = []
    for highlight in highlights:
        if with_headings and highlight.heading not in added_headings and len(highlight.heading) > 0:
            text += '---\n## ' + highlight.heading + '\n'
            added_headings.append(highlight.heading)
        text += '> {}\n\n'.format(highlight.text.replace('\n', '\n> '))
    return text
