# -*- coding: utf-8 -*-

import re 

# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))

def generate_md(title, highlights, with_headings=True, normal_sorting=True):
        text = '# {}\n\n'.format(title)
        if normal_sorting:
            highlights = sorted(highlights, key=(lambda highlights: (highlights[3], highlights[4], highlights[2])), reverse=False) # sort by chapter, reference in chapter and creation time
        added_headings = []
        for highlight in highlights:
            if with_headings and highlight[1] not in added_headings:
                text += '---\n## ' + highlight[1] + '\n'
                added_headings.append(highlight[1])
            text += '> {}\n\n'.format(highlight[0].replace('\n', '\n> '))
        return text