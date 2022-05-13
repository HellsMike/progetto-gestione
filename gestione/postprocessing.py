import json
import os
import re
from nltk import word_tokenize, download
from nltk.corpus import stopwords
import simplemma
from whoosh import index
from whoosh.fields import Schema, STORED, TEXT


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

    if not os.path.exists('static/index_lemm_boost'):
        os.mkdir('static/index_lemm_boost')

    ix = index.create_in('static/index_lemm_boost', schema)
    writer = ix.writer(limitmb=2048, procs=4)

    for collection in (giallo_collection, donna_collection):
        with open(f'static/collections/{collection}') as file:
            content = json.load(file)
        for recipe in content:
            writer.add_document(fonte=recipe['fonte'], categoria=recipe['categoria'], titolo=f"{recipe['titolo']}",
                                ricetta_link=recipe['ricetta_link'], ingredienti=recipe['ingredienti'],
                                ingredienti_token=tokenize(recipe['ingredienti_token']),
                                preparazione=recipe['preparazione'], immagine_src=recipe['immagine_src'])

    writer.commit()


'''Sistema le collection di documenti'''
def json_fix():
    giallo_collection = 'giallozafferano.json'
    donna_collection = 'donnamoderna.json'
    
    for collection in (giallo_collection, donna_collection):
        url = f'static/collections/{collection}'
        
        with open(url, encoding='utf-8') as file:
            content = json.load(file)
        
        '''Cicla i documenti presenti nel json'''
        for document in content:
            '''Esegue l\'operazione per ogni campo elaborato ("grouped" a Web Scraper)'''
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
