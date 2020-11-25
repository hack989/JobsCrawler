import requests as r
import lxml.html
import csv
import json

__author__ = "jebas Raja"


def getresponse(link):
    resp = r.get(url=link, timeout=10)
    return lxml.html.fromstring(resp.content)


def parse_job(joblink):
    try:
        print("crawling: {}".format(joblink))
        response = getresponse(joblink)
        job = {}
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]')[0].text_content().encode('utf-8', 'ignore').decode(
                'utf-8'))
        job["title"] = data.get("title", None)
        job['location'] = data.get('jobLocation')[0].get('address').get('addressLocality')
        job['datePosted'] = data.get('datePosted', None)
        job['employmentType'] = data.get('employmentType', None)
        job['skills'] = data.get('skills', None)

        with open('stackjobs.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['title', 'location', 'datePosted', 'employmentType', 'skills'])
            writer.writerow(job)

    except Exception as ex:
        print(str(ex))


if __name__ == "__main__":

    print("--------------Stackoverflow spider started Crawling -----------------")

    seedurl = "https://stackoverflow.com"
    startingurl = "https://stackoverflow.com/jobs?pg={}"

    for i in range(1, 42):
        try:
            print("---------------Crawling page #:{}--------------------".format(i))
            resp = r.get(url=startingurl.format(i), timeout=10)
            tree = lxml.html.fromstring(resp.content)
            links = tree.xpath('//a[@class="s-link stretched-link"]')
            for link in links:
                parse_job(seedurl + link.attrib['href'])
            print("---------------Finished Crawling page #:{}--------------------".format(i))
        except Exception as e:
            print(str(e))
