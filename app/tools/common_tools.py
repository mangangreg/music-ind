#!/usr/bin/env python
'''
author: Greg Mangan
description: Common tools across the ETL for musicbrainapp
'''
wiki_base_url = 'http://en.wikipedia.org'

def gen_id(url):
    ''' Generate an 8-digit id (int) for based on the  url'''
    return hashlib.sha512(url.encode('utf-8')).hexdigest()[:10]