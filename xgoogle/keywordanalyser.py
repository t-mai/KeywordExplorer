"""
Analyse Google search results and return important keywords
"""

from scraper import GoogleScraper, ScraperError
from alchemyapi import AlchemyAPI

class Frequency(object):
    def __init__(self, word, title, frequency):
        self.word = word
        self.title = title
        self.frequency = frequency
    
    def __str__(self):
        return "the word '%s' appears in the title '%s' %s times" % (self.word, self.title, self.frequency)


class Keyword(object):
    def __init__(self, word, score):
        self.word = word
        self.score = score

    def __str__(self):
        return "Keyword word: '%s'. Relevant score: %s" % (self.word, self.score)

    def get_score(self):
        return self.score
    
    def  get_pharse(self):
        return self.word

class ScraperResult(object):
    def __init__(self, urls, titles, descriptions, contents):
        self.urls = urls
        self.titles = titles
        self.descriptions = descriptions
        self.contents = contents
    def __str__(self):
        return "Data from scraping %s urls" % len(urls)

class KeywordAnalyser(object):
    def __init__(self, query, numofresults=10, numberofkeywords=10):
        self.query = query
        self.numberofkeywords = numberofkeywords
        self.scraper = GoogleScraper(query, random_agent=True, debug=True)
        self.scraper.results_per_page = numofresults

    def scrap_data(self):
        """Scrap data from google search results"""
        sresults = self.scraper.get_results()
        urls = []
        titles = []
        descriptions = []
        contents = []

        for result in sresults:
            urls.append(result.url.encode("utf8"))
            titles.append(result.title.encode("utf8"))
            descriptions.append(result.desc.encode("utf8"))
            contents.append(result.content.encode("utf8"))
        
        return ScraperResult(urls,titles,descriptions,contents)

    def extract_keyword_alchemy(self, corpus):
        alchemyapi = AlchemyAPI()

        corpus_text = "\n".join(corpus)

        response = alchemyapi.keywords('text', corpus_text, {'sentiment': 1})

        keywords = []
        if response['status'] == "OK":
            for keyword in response['keywords']:
                pharse = keyword['text'].encode('utf8')
                score = float(keyword['relevance'].encode('utf8'))
                kw = Keyword(pharse, score)
                keywords.append(kw)

        sorted_keywords = sorted(keywords, key=lambda t: t.get_score() * -1)
        
        return sorted_keywords[:min(len(sorted_keywords), self.numberofkeywords)]
