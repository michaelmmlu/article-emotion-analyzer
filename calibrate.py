import requests
import bs4
import string
import newspaper

def prelim_scrape(url):
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    script = soup.findAll(['script', 'style', 'a', 'button', 'label', 'time', 'caption', 'figcaption', 'li'])
    for match in script:
        match.decompose()
    txt = ""
    lst = soup.get_text().splitlines()
    for line in lst:
        txt += line + " "
    txt = ' '.join(txt.split())
    return txt

def get_min_max(text):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types

    client = language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    entities = client.analyze_entity_sentiment(document)

    max_mag, min_mag = 0, 0

    for entity in entities:
        if entity.sentiment.magnitude > max_mag:
            max_mag = entity.sentiment.magnitude
        elif entity.sentiment.magnitude < min_mag:
            min_mag = entity.sentiment.magnitude

    return min_mag, max_mag, len(text)

urls = ['http://www.cnn.com/', 'http://www.nytimes.com/', 'http://www.thehill.com/', 'http://www.foxnews.com/', 'https://www.usatoday.com/']

full_urls = []

data = []

for url in urls:
    temp = newspaper.build(url)
    i = 0
    for full_url in temp.articles:
        if i == 20:
            break
        full_urls.append(full_url.url)
        i += 1

print(full_urls)

# for url in full_urls:
#     text = prelim_scrape(url)
#     data.append(get_min_max(text))
#
# txtfile = open("data.txt", "w")
# for dpoint in data:
#     txtfile.write(dpoint + '\n')
