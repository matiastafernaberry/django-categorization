import spacy

nlp = spacy.load("es_core_news_sm")
doc = nlp("River: la prioridad de Gallardo es conservar el plantel")

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)