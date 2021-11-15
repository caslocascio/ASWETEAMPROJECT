import requests
from bs4 import BeautifulSoup
import re


def getProfReview(Url, prof_name):
    page = requests.get(Url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="card text-center")
    cards = results.find_all("div", class_="card")
    for c in cards:
        title = c.find("h5", class_="card-title").text
        date = c.find("h6", class_="card-subtitle").text
        review = c.find("p", class_="card-text").text[8:] \
            .replace("\n", "\\n").replace('"', '""')
        workload = c.find("p", class_="card-subtitle").text[10:] \
            .replace("\n", "\\n").replace('"', '""')
        m = re.search(r'Agree: (\d+) \| Disagree: (\d+) \| Funny: (\d+)',
                      c.text)
        yield '"%s","%s","%s","%s","%s",%s,%s,%s\n' % \
            (prof_name, title, date, review, workload,
             m.group(1), m.group(2), m.group(3))


def getProfs(Url):
    page = requests.get(Url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("div", class_="col-sm-4 overflow-auto p-3 bg-light")
    return results.find_all("a")


if __name__ == "main":
    with open("culpa.csv", "w") as f:
        BaseURL = "https://culpaarchive.herokuapp.com"
        profs = getProfs(BaseURL)
        print("total:" + str(len(profs)))
        f.write('"professor","class","date","review","workload","agree", \
                "disagree","funny"\n')
        cnt = 1
        for prof in profs:
            result = getProfReview(BaseURL + prof['href'], prof.text)
            for txt in result:
                f.write(txt)
            print("\r" + str(cnt) + " done", end="", flush=True)
            cnt += 1
