# THIS CODE IS CURRENTLY UNDER DEVELOPMENT AND IS UPDATED REGULARLY.
# This is a search engine under development.
# THE FOLLOWING IS A LOG OF UPDATES:
# 11-17-18: Updated crawl_web, lookup & add_to_index to use hash table data structure instead of list-based structure
# 10-30-18: added record_user_click and modified add_to_index to include click count capability
# 10-24-18: reverted add_to_index and lookup() and impoved add_to_index by removing duplicate URLs
# 10-23-18: defined get_page using urllib library, edited def add_to_index to increase speed, edited lookup (decreases speed)
# 10-19-18: revised crawl_web to include indexing capability
# 10-18-18: defined add_page_to_index, which breaks page content into keywords, then calls add_to_index
# 10-14-18: added indexing/keyword association capability via add_to_index, also defined lookup function
# 10-9-18: defined crawl_web()
# 10-8-18: improved get_all_links() by calling newly defined function union()
# 10-2-18: defined get_all_links()
# 9-28-18: log start date; defined get_next_target()

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def record_user_click(index, keyword, url):
	urls = lookup(index, keyword)
	if urls:
		for entry in urls:
			if entry[0] == url:
				entry[1] += 1


def add_to_index(index, keyword, url):
    if keyword in index:
    	index[keyword].append(url)
    else:
    	index[keyword] = [url]

def lookup(index, keyword):
    if keyword in index:
    	return index[keyword]
    else:
    	return None

def split_string(source, splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] += char
    return output

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def crawl_web(seed):
    tocrawl = [seed]
    crawled = []
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl,get_all_links(content))
            crawled.append(page)
    return index
