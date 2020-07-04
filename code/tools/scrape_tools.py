url_list_of_lists = 'http://en.wikipedia.org/wiki/List_of_Billboard_Hot_100_top-ten_singles'
wiki_base_url = 'http://en.wikipedia.org'

def gen_id(wiki_url):
    ''' Generate an 8-digit id (int) for based on the unique wikipedia url'''
    return hash(wiki_url) % 10**8

def clean_text(string):
    ''' Clean common cell text from a <td> tag '''
    return string.replace('\xa0', ' ').replace('\n',' ').strip()

def missing_link(name, soup):
    ''' Find a hpyerlink for a given name '''
    if soup.find('a', text=name):
        return soup.find('a', text=name).attrs.get('href')
    else:
        return None

def get_hyper_list(td, soup):
    '''
        Extract names and URLs from horizontal lists of hyperlinks

        Inputs:
            td (bs4 tag)
    '''
    result_list = []
    if not td.find('ul'):
        return [{'name': td.text, 'url':None, 'order': 0}]
    else:
        result_list = []
        for i, li in enumerate(td.find_all('li')):
            name = li.text
            url = li.find('a').attrs.get('href') if li.find('a') else missing_link(name, soup)
            result_list.append({'name': name, 'url': url, 'order': i})

        return result_list
