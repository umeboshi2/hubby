import random
import time
import datetime
import urlparse
import urllib2
from httplib import IncompleteRead

from hubby.legistar import legistar_host


class FileExistsError(Exception):
    pass


class BadDownloadError(Exception):
    pass


class InvalidDateFormat(Exception):
    pass

# Tidy function inspired by:
# http://www.toao.net/48-replacing-smart-quotes-and-em-dashes-in-mysql


def tidy_needless_utf_punctuation(data):
    data = data.replace('\xe2\x80\x98', "'")
    data = data.replace('\xe2\x80\x99', "'")
    data = data.replace('\xe2\x80\x9c', '"')
    data = data.replace('\xe2\x80\x9d', '"')
    data = data.replace('\xe2\x80\x93', "-")
    data = data.replace('\xe2\x80\x94', "--")
    data = data.replace('\xe2\x80\xa6', "...")
    return data


def random_wait(minimum=5, maximum=15, msg=''):
    #seconds = random.randint(minimum, maximum)
    seconds = random.random() * 5 + 1
    if msg:
        template_data = dict(seconds=seconds)
        msg = msg % template_data
        print msg
    time.sleep(seconds)


def parse_date_string(datestring):
    dlist = datestring.split('/')
    if len(dlist) != 3:
        raise InvalidDateFormat("Invalid date string: %s" % datestring)
    dlist = map(int, dlist)
    proper = dlist[2], dlist[0], dlist[1]
    return proper


def make_true_date(datestring):
    proper = parse_date_string(datestring)
    return datetime.date(*proper)


def parse_legistar_cgi_query(link):
    uparse = urlparse.urlparse(link)
    query = uparse.query
    item_split = query.split('&')
    items = [item.split('=') for item in item_split]
    parsed = dict(items)
    return parsed


def legistar_id_guid(link):
    plink = parse_legistar_cgi_query(link)
    id = int(plink['ID'])
    guid = plink['GUID']
    return id, guid


def onclick_link(attribute):
    return attribute.split("'")[1]


def rss_entry_updated(entry):
    uparsed = entry.updated_parsed
    updated = datetime.datetime(*uparsed[:6])
    return updated


def _view_url(id, guid, type):
    """Returns the url for for the agenda(A)/minutes(M) from a meeting identified
    by id, guid"""
    host = legistar_host
    url_template = 'http://%s/View.ashx?M=%s&ID=%d&GUID=%s'
    url = url_template % (host, type, id, guid)
    return url


def agenda_url(id, guid):
    """Returns the url for for the agenda from a meeting identified
    by id, guid"""
    return _view_url(id, guid, 'A')


def minutes_url(id, guid):
    """Returns the url for for the agenda from a meeting identified
    by id, guid"""
    return _view_url(id, guid, 'M')


#################################
#################################
#################################
#################################
# Handle download stuff below
#################################
#################################
#################################
#################################
#################################
def handle_link(uri):
    data = dict()
    attachment_marker = 'attachment;'
    filename_marker = 'filename='
    disposition_key = 'content-disposition'
    length_key = 'content-length'
    f = urllib2.urlopen(uri)
    info = f.info()
    data['info'] = info
    data['fileobj'] = f
    # presume no attachment first
    data['attachment'] = False
    if disposition_key in info:
        disposition = info[disposition_key]
        if disposition.startswith(attachment_marker):
            data['attachment'] = True
            fragment = disposition.split(attachment_marker)[1]
            filename = fragment.split(filename_marker)[1]
            length = int(info[length_key])
            data['filename'] = filename
            data['length'] = length
    return data


def get_rss_feed(url):
    response = urllib2.urlopen(url)
    read_it = True
    content = ''
    while read_it:
        try:
            content += response.read(1)
        except IncompleteRead:
            read_it = False
    return content, response.info()


if __name__ == "__main__":
    import os
