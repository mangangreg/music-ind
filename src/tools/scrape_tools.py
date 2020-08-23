import hashlib
import re
import pdb

url_list_of_lists = 'http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles'
wiki_base_url = 'http://en.wikipedia.org'

re_citation = r"\[\d{1,3}\]"

def gen_id(wiki_url):
    ''' Generate an 8-digit id (int) for based on the unique wikipedia url'''
    return hashlib.sha512(wiki_url.encode('utf-8')).hexdigest()[:10]
    # return hash(wiki_url) % 10**8

def clean_text(string):
    ''' Clean common cell text from a <td> tag '''
    string = string.replace('\xa0', ' ').replace('\n',' ')
    string = re.sub(re_citation, '', string).strip()
    return string

def missing_link(name, soup):
    ''' Find a hpyerlink for a given name '''
    if soup.find('a', text=name):
        return soup.find('a', text=name).attrs.get('href')
    else:
        return None

def extract_list(td, soup):
    '''
        Extract names and URLs from horizontal lists of hyperlinks

        Inputs:
            td (bs4 tag)
    '''
    result_list = []
    classes = td.attrs.get('class', '')
    # ul case
    if 'hlist' in classes:
        for i, li in enumerate(td.find_all('li')):
            name = clean_text(li.text)
            url = li.find('a').attrs.get('href') if li.find('a') else missing_link(name, soup)
            result_list.append({'name': name, 'url': url, 'order': i})

    # One big list case
    else :
        # Parse "a,b, and c" text case
        if ',' and 'and' in td.text:
            # Split apart from the last 'and'
            it = re.finditer(r'and', td.text)
            a1, a2 = list(it)[-1].span()

            nlist = [clean_text(x) for x in (td.text[:a1] + ',' + td.text[a2:]).split(',')]

            for i, name in enumerate(nlist):
                url = missing_link(name, td)
                result_list.append({'name': name, 'url': missing_link(name, soup), 'order': i})
    # Just text
        else:
            name = clean_text(td.text)
            result_list.append({'name': name , 'url':missing_link(name, soup), 'order': 0})
    return result_list
