import urllib.request,ast,requests,re
from bs4 import BeautifulSoup
from lxml import etree



def return_html(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()
    source = mybytes.decode("utf8")
    return source

def html_from_query(query):
    base_url = "https://web.stagram.com/search?query="
    return return_html(base_url+query)

def get_usernames(query):
    html = html_from_query(query)
    soup = BeautifulSoup(html, "html.parser" )
    frame_div = soup.findAll('div', attrs={'class':'row photolist'})
    newsoup = BeautifulSoup(str(frame_div), "html.parser" )
    unames = []
    for a in newsoup.find_all('a', href=True):
        url = a['href']
        length = len(url.split("/")) - 1
        if not length > 1:
            uname = url[1:]
            unames.append(uname)
    return unames

def get_bio(handle, proxies=None):
    url = 'https://www.instagram.com/{}/'.format(handle)
    attributes = {}
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    if response.ok:
        root = etree.HTML(response.content)
        data_raw = root.xpath("//script[contains(text(), 'entry_data')]")[0].text
        data_raw = data_raw[data_raw.find('{'): data_raw.rfind('}') + 1]
        data_raw = data_raw.replace('false', 'False')
        data_raw = data_raw.replace('true', 'True')
        data_raw = data_raw.replace('null', 'None')
        data_dict = ast.literal_eval(data_raw)
        d=data_dict['entry_data']['ProfilePage'][0]['graphql']['user']
        bio = d['biography']
        return repr(bio)

def get_emails(uname):
    bio = get_bio(uname)
    r = re.compile(r"(\w(?:[-.+]?\w+)+\@(?:[a-z0-9](?:[-+]?\w+)*\.)+[a-z]{2,})", re.I)
    regex = r.findall(bio)
    if bool(regex):
        #print(regex)
        print("[+] "+uname)
        print(" |  "+"\n[+] ".join(regex))

def return_list(unames_string):
    all_unames = []
    unames_string = unames_string.split(",")
    for uname in unames_string:
        all_unames += get_usernames(uname.strip())
    return all_unames

if __name__ == "__main__":
    hashtags = "hashtag1,hashtag2,hashtag3"
    all_unames = return_list(
    
    )
    for uname in all_unames:
        get_emails(uname)
    print("[e] End")
