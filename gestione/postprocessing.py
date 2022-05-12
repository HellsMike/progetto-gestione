import json
import re
from turtle import down
from nltk import word_tokenize, download
from nltk.corpus import stopwords
import simplemma


def tokenize(value):
    tokens = []
    langdata = simplemma.load_data("it")

    while True:
        try:
            tokenized_value = word_tokenize(value, language="italian")
            for token in tokenized_value:
                if not token in stopwords.words("italian") and token.isalnum():
                    tokens.append(simplemma.lemmatize(token, langdata))
                    tokens.append(token)
            return tokens
        except LookupError:
            download('punkt')
            download('stopwords')


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
                values = json.loads(values) #Legge i valori dei campi (dizionario) come json per unirli in una singola stringa
                new_string = ''

                for value in values:
                    new_string += value[key] + ', '
                document[key] = new_string[:-2]

        with open(url, 'w', encoding='utf-8') as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
