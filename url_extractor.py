import re
from urllib.parse import urljoin, urlsplit, SplitResult
import requests
from bs4 import BeautifulSoup
import string


class RecursiveScraper:
    def __init__(self, url):
      
        self.domain = urlsplit(url).netloc
        self.mainurl = url
        self.urls = set()

    def preprocess_url(self, referrer, url):
       
        if not url:
            return None

        fields = urlsplit(urljoin(referrer, url))._asdict()
        fields['path'] = re.sub(r'/$', '', fields['path']) 
        fields['fragment'] = '' 
        fields = SplitResult(**fields)
        if fields.netloc == self.domain:
         
            if fields.scheme == 'http':
                httpurl = cleanurl = fields.geturl()
                httpsurl = httpurl.replace('http:', 'https:', 1)
            else:
                httpsurl = cleanurl = fields.geturl()
                httpurl = httpsurl.replace('https:', 'http:', 1)
            if httpurl not in self.urls and httpsurl not in self.urls:
               
                return cleanurl

        return None

    def scrape(self, url=None):
       
        if url is None:
            url = self.mainurl

        print("{:s} ...".format(url))
        self.urls.add(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        for link in soup.findAll("a"):
            childurl = self.preprocess_url(url, link.get("href"))
            if childurl:
                self.scrape(childurl)


if __name__ == '__main__':
    rscraper = RecursiveScraper(input())
    rscraper.scrape()
    print(rscraper.urls)
    new= list(rscraper.urls)
    print(new)
    for i in new:
        print(i)
        
   
        r = requests.get(i)
        soup = BeautifulSoup(r.content, "html.parser")

        for script in soup(["script", "style"]):
            script.extract()  
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        new = text.encode("utf-8")
        final=new.decode("utf-8")
        new1=final.lower()
        s="".join([w for w in new1 if w not in string.punctuation])
        print(s)

