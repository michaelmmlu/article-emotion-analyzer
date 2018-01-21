import requests
import bs4
from newspaper import Article
from flask import Flask, redirect, request, render_template, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

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

def rating(score):
    if score >= 0.7:
        return "extremely positively biased"
    elif score >= 0.3:
        return "moderately positively biased"
    elif score >= 0.05:
        return "sligtly positively biased"
    elif score < 0.05 and score > -0.05:
        return "neutral/mixed"
    elif score <= -0.7:
        return "extremely negatively biased"
    elif score <= -0.3:
        return "moderately negatively biased"
    elif score <= -0.05:
        return "slightly negatively biased"

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

    # for i in range(7):
    #     temp = []
    #     for entity in entity_sent.entities:
    #         if entity.type == i + 1:
    #             temp.append(entity)
    #     sorted_entities.append(temp)
    temp = []
    for entity in entity_sent.entities:
        temp.append(entity)
    entity_sent = temp

    for ent in entity_sent:
        i = 0
        while i < len(entity_sent):
            reference = entity_sent[i].name
            j = i + 1
            while j < len(entity_sent):
                if entity_sent[j].name == reference or entity_sent[j].name + 's' == reference or entity_sent[j].name == reference + 's':
                    entity_sent.pop(j)
                else:
                    j += 1
            i += 1

    new_list = []
    new_list.extend([rating(sentiment.score)])

    i = 0
    for entity in entity_sent:
        if i == 5:
            break
        new_list.extend([entity.name, rating(entity.sentiment.score)])

    return new_list

    # for type in sorted_entities:
    #     for entity in type:
    #         print(entity.name, types[entity.type], entity.salience, entity.sentiment.score, entity.sentiment.magnitude)
    #
    # print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

# @app.route('/')
# def homepage():
#     return render_template('popup.html')

@app.route('/run_analysis', methods = ['GET', 'POST'])
def run_analysis():

    form_url = request.form['form_url']

    text = scrape_analyze(form_url)
    lst = analyze(text)
    string = ""
    for i in lst:
        string += str(i) + ","

    return json.dumps(string)

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
