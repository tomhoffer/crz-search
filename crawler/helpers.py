import hashlib


def hash_url(url: str):
    return hashlib.md5(url.encode()).hexdigest()


def remove_url_trailing_slash(url: str):
    return url.rstrip('/')

def generate_start_urls():
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    years = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']
    start_urls = []

    for y in years:
        for i in range(len(months)):
            try:
                start_urls.append("https://www.crz.gov.sk/2171273-sk/centralny-register-zmluv/?art_datum_zverejnene_od=01.{}.{}&art_datum_zverejnene_do=01.{}.{}&page=0".format(months[i], y, months[i+1], y))
            except IndexError:
                start_urls.append("https://www.crz.gov.sk/2171273-sk/centralny-register-zmluv/?art_datum_zverejnene_od=01.{}.{}&art_datum_zverejnene_do=01.{}.{}&page=0".format(months[i], y, months[i], y))

    return start_urls
