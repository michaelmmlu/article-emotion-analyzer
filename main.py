import requests
import bs4
from newspaper import Article
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

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

def scrape_analyze(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def analyze(text):
    from google.cloud import language_v1
    from google.cloud.language import enums
    from google.cloud.language import types

    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects sentiment for entire article and top five salient entities
    sentiment = client.analyze_sentiment(document).document_sentiment
    entity_sent = client.analyze_entity_sentiment(document)

    sorted_entities = []

    types = {0: 'Unknown', 1: 'Person', 2: 'Location', 3: 'Organization', 4: 'Event', 5: 'Work of art', 6: 'Consumer good', 7: 'Other'}

    for i in range(7):
        temp = []
        for entity in entity_sent.entities:
            if entity.type == i + 1:
                temp.append(entity)
        sorted_entities.append(temp)

    for lst in sorted_entities:
        i = 0
        while i < len(lst):
            reference = lst[i].name
            j = i + 1
            while j < len(lst):
                if lst[j].name == reference or lst[j].name + 's' == reference or lst[j].name == reference + 's':
                    lst.pop(j)
                else:
                    j += 1
            i += 1

    sorted_entities.append([sentiment.score, sentiment.magnitude])

    return sorted_entities

    # for type in sorted_entities:
    #     for entity in type:
    #         print(entity.name, types[entity.type], entity.salience, entity.sentiment.score, entity.sentiment.magnitude)
    #
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

@app.route('/')
def homepage():
    return render_template('popup.html')

@app.route('/run_analysis', methods = ['GET', 'POST'])
def run_analysis():

    form_url = request.form['url']

    text = scrape_analyze(form_url)
    return render_template('popup.html', sorted_entities = analyze(text))

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
