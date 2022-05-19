import json
import os
import re
from nltk import word_tokenize, download
from nltk.corpus import stopwords, wordnet
import simplemma
from whoosh import index
from whoosh.qparser import MultifieldParser
from whoosh.fields import Schema, STORED, TEXT


# Sistema le collection di documenti
def json_fix():
    giallo_collection = 'giallozafferano.json'
    donna_collection = 'donnamoderna.json'
    
    for collection in (giallo_collection, donna_collection):
        url = f'static/collections/{collection}'
        
        with open(url, encoding='utf-8') as file:
            content = json.load(file)
        
        # Cicla i documenti presenti nel json
        for document in content:
            # Esegue l\'operazione per ogni campo elaborato ("grouped" a Web Scraper)
            for key in ('ingredienti', 'ingredienti_token', 'preparazione'):
                values = document[key].replace('\\t', '').replace('\\n', ' ')
                values = re.sub(' +', ' ', values)
                # Legge i valori dei campi (dizionario) come json per unirli in una singola stringa
                values = json.loads(values)
                new_string = ''

                for value in values:
                    new_string += value[key] + ', '
                document[key] = new_string[:-2]

        with open(url, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)


def tokenize(value):
    tokens = []
    langdata = simplemma.load_data("it")

    while True:
        try:
            tokenized_value = word_tokenize(value, language="italian")
            for token in tokenized_value:
                if token not in stopwords.words("italian") and token.isalnum():
                    tokens.append(simplemma.lemmatize(token, langdata))
                    tokens.append(token)
            return tokens
        except LookupError:
            download('punkt')
            download('stopwords')


def indexing():
    giallo_collection = 'giallozafferano.json'
    donna_collection = 'donnamoderna.json'
    schema = Schema(fonte=STORED, categoria=TEXT(stored=True), titolo=TEXT(stored=True, field_boost=2.0),
                    ricetta_link=STORED, ingredienti=STORED, ingredienti_token=TEXT(stored=False), preparazione=STORED,
                    immagine_src=STORED)

    if not os.path.exists('static/indices/index_full'):
        os.makedirs('static/indices/index_full')

    indx = index.create_in('static/indices/index_full', schema)
    writer = indx.writer(limitmb=2048, procs=4)

    for collection in (giallo_collection, donna_collection):
        with open(f'static/collections/{collection}', encoding='utf-8') as file:
            content = json.load(file)
        for recipe in content:
            writer.add_document(fonte=recipe['fonte'], categoria=recipe['categoria'], titolo=f"{recipe['titolo']}",
                                ricetta_link=recipe['ricetta-link'], ingredienti=recipe['ingredienti'],
                                ingredienti_token=tokenize(recipe['ingredienti_token']),
                                preparazione=recipe['preparazione'], immagine_src=recipe['immagine-src'])

    writer.commit()


def parsing(base_query, field, is_syn, page=1):
    new_query = base_query
    expression = re.compile("#[^\s]*")
    matches = expression.findall(new_query)

    if len(matches) > 0:
        for match in matches:
            new_query = new_query.replace(match, synonyms_get(match[1:]))
    else:
        num_of_words = len(base_query.split(' '))
        if num_of_words == 1 and is_syn == 'syn':
            new_query = synonyms_get(base_query)

    if field == 'tutto':
        fields = ['titolo', 'categoria', 'ingredienti_token']
    elif field == 'ingredienti':
        fields = ['ingredienti_token']
    else:
        fields = [field]

    indx = index.open_dir('static/indices/index_full')
    multi_parser = MultifieldParser(fields, schema=indx.schema)
    parsed_query = multi_parser.parse(new_query.encode('utf-8'))
    searcher = indx.searcher()
    results = searcher.search_page(parsed_query, page, pagelen=24)

    return results


# Ricerca per sinonimi
def synonyms_get(word):
    synonyms = [word]
    while True:
        try:
            for synonym in wordnet.synsets(word, lang="ita"):
                for word_lemmatized in synonym.lemmas(lang="ita"):
                    if word_lemmatized.name() != word:
                        synonyms.append(word_lemmatized.name())
            return f'({" OR ".join(synonyms)})'
        except:
            download('wordnet')
            download('omw-1.4')
            