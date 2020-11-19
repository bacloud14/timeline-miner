import re
import logging
from daterangeparser import parse

def dep_subtree(token, dep):
    deps = [child.dep_ for child in token.children]
    child = next(filter(lambda c: c.dep_ == dep, token.children), None)
    if child != None:
        return ' '.join([c.text for c in child.subtree])
    else:
        return ''

# to remove citations, e.g. "[91]" as this makes problems with spaCy
p = re.compile(r'\[\d+\]')

def extract_events_spacy(line, nlp):
    line = p.sub('', line)
    events = []
    doc = nlp(line)
    for ent in filter(lambda e: e.label_ == 'DATE', list(doc.ents)):
        try:
            (start, end) = parse(ent.text)
        except Exception as e:
            logging.debug(e)
      # could not parse the dates, hence ignore it

            continue
        current = ent.root
        while current.dep_ != 'ROOT':
            current = current.head
        desc = ' '.join(filter(None, [
            dep_subtree(current, 'nsubj'),
            dep_subtree(current, 'nsubjpass'),
            dep_subtree(current, 'auxpass'),
            dep_subtree(current, 'amod'),
            dep_subtree(current, 'det'),
            current.text,
            dep_subtree(current, 'acl'),
            dep_subtree(current, 'dobj'),
            dep_subtree(current, 'attr'),
            dep_subtree(current, 'advmod'),
            ]))
        events = events + [(start, ent.text, desc)]
    return events

import numpy as np
import datetime

def std(arrays):
    total = 0
    for arr in arrays:
        total+=np.std(np.array(arr))
    return (total)
def splitter(arr):
    for i in range(1, len(arr)):
        start = arr[0:i]
        end = arr[i:]
        if(len(start) < 2 or len(end) < 2):
            continue
        yield (start, end)
        for split in splitter(end):
            result = [start]
            result.extend(split)
            yield result

def get_best_split(timeline, text):
    a = np.array([(datetime.datetime.utcnow() - date[0]).days for date in timeline])[:15]
    reverse_timeline = dict(zip(a, timeline))
    minimum = 999999999
    best_split = None
    for split in splitter(a):
        std_ = std(split)
        if(std_ < minimum):
            minimum = std_
            best_split = split
    stacked_result = []
    best_split = [list(arrayLike) for arrayLike in best_split]
    logging.debug(best_split)
    flattened = [[item, best_split.index(sublist)] for sublist in best_split for item in sublist]
    for key in flattened:
        category = key[1]
        key_ = key[0]
        mined = reverse_timeline[key_][2]
        sentence_ = ""
        if(len(mined)<60):
            text = split_into_sentences(str(text))
            for sentence in text:                
                if( mined in sentence):
                    sentence_ = sentence
        
        stacked_result.append({
                "date":reverse_timeline[key_][1], 
                "play":mined[:80]+"...",
                "event":mined,
                "full":sentence_,
                "category":category
            })
    return stacked_result


import re
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences