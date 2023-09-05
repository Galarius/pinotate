import re 
from datetime import datetime, timedelta, timezone


# source: https://github.com/django/django/blob/master/django/utils/text.py
def valid_filename(s):
    return re.sub(r'(?u)[^-\w.]', '', str(s).strip().replace(' ', '_'))

def datetime_to_local(seconds_since_ref_date):
    reference_date = datetime(2001, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    delta_since_reference = timedelta(seconds=seconds_since_ref_date)
    utc = (reference_date + delta_since_reference)
    local_time = utc.astimezone()
    return local_time.strftime('%c')

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
