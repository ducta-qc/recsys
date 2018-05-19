import requests
import urllib
from lxml import html
import json

imdb_host = 'https://imdb.com'


def get_movie(movie_title):
    movie = {}
    query = urllib.quote_plus(movie_title)
    page_content = requests.get(
        'https://www.imdb.com/find?ref_=nv_sr_fn&q=%s&s=all' % query
    )
    tree = html.fromstring(page_content.content)
    first_result = tree.xpath("//td[@class='result_text']/a[1]/@href")[0]

    # get movie url
    movie_id = first_result.split("/")[2]
    movie_url = "%s%s" % (imdb_host, first_result)
    movie_detail = requests.get(movie_url)

    tree = html.fromstring(movie_detail.content)
    director = tree.xpath("//span[@itemprop='director']/a[1]/span[1]/text()")
    director_id = tree.xpath("//span[@itemprop='director']/a[1]/@href")
    director_id = [x.split("/")[2] for x in director_id]
    country = tree.xpath("//div[@class='article']/div[@class='txt-block'][1]/a[1]/text()")[0]
    language = tree.xpath("//div[@class='article']/div[@class='txt-block'][2]/a[1]/text()")[0]
    cast_content = requests.get(
        "%s/title/%s/fullcredits?ref_=tt_cl_sm#cast" % (imdb_host, movie_id)
    )
    tree = html.fromstring(cast_content.content)
    cast_members = tree.xpath("//td[@itemprop='actor']/a[1]/span[1]/text()")
    cast_members_id = tree.xpath("//td[@itemprop='actor']/a[1]/@href")
    cast_members_id = [x.split("/")[2] for x in cast_members_id]
    keyword_content = requests.get(
        "%s/title/%s/keywords?ref_=tt_stry_kw" % (imdb_host, movie_id)
    )
    tree = html.fromstring(keyword_content.content)
    keywords = tree.xpath("//div[@class='sodatext']/a[1]/text()")
    
    movie['imdb_id'] = movie_id
    movie['director'] = {}
    for k, v in zip(director_id, director):
        movie['director'][k] = v
    movie['country'] = country
    movie['language'] = language
    movie['cast_members'] = {}
    for k, v in zip(cast_members_id, cast_members):
        movie['cast_members'][k] = v
    movie['keywords'] = keywords
    return movie

# result = get_movie("Kronos (1957)")

# buf = json.dumps(result, indent=4, sort_keys=True)
# print(buf)