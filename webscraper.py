import requests
import bs4
import string

def scrape(site):
    res = requests.get(site)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    script = soup.findAll(['script', 'style', 'a', 'button', 'label', 'time'])
    for match in script:
        match.decompose()
    txt = ""
    lst = soup.get_text().splitlines()
    for line in lst:
        if all(c in string.printable for c in line):
            txt += line + " "
        else:
            txt += line.encode('cp850', 'replace').decode('cp850') + " "
    txt = ' '.join(txt.split())
    return txt

if __name__ == '__main__':
    text = scrape('https://www.theguardian.com/world/2018/jan/19/frosty-reception-for-south-koreas-winter-olympics-detente-with-north')

    txtfile = open('list.txt', 'w')
    txtfile.write(text)
