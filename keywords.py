import spacy
import subprocess
from string import punctuation
from url_extractor import RecursiveScraper, rscraper

def extract_keywords(nlp, sequence, special_tags : list = None):
  
    result = []

    pos_tag = ['PROPN','NOUN','ADJ']

    doc = nlp(sequence.lower())
    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)
    
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))

if __name__ == "__main__":
    subprocess.call("python -m spacy download en_core_web_sm",shell=True)
    nlp = spacy.load("en_core_web_sm")
    print(extract_keywords(nlp,"""Learning how to use natural language
   processing in python and build Flask API's is easy when you have packages like spacy and fuzzywuzzy""")) # test if it works
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
        print(extract_keywords(nlp, s))
