# -*- coding: utf-8 -*-

import re 
from datetime import datetime, timedelta
from dateutil import tz

# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))

def datetime_to_local(seconds_since_ref_date):
    reference_date = datetime(2001, 1, 1, 0, 0, 0)
    delta_since_reference = timedelta(seconds=seconds_since_ref_date)
    utc = (reference_date + delta_since_reference)
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone).strftime('%c')

def generate_md(title, highlights, with_headings=True, normal_sorting=True):
    text = '# {}\n\n'.format(title)    
    if normal_sorting:
        highlights = sorted(highlights, key=(lambda highlight: (highlight.chapter, highlight.ref_in_chapter, highlight.created)), reverse=False)
    added_headings = []
    for highlight in highlights:
        if with_headings and highlight.heading not in added_headings and len(highlight.heading) > 0:
            text += '---\n## {}\n'.format(highlight.heading)
            added_headings.append(highlight.heading)
        text += '*{}*\n'.format(datetime_to_local(highlight.created))
        text += '> {}\n\n'.format(highlight.text.replace('\n', '\n> '))
    return text
