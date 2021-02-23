import stanza
#stanza.download('es')
nlp = stanza.Pipeline(lang='es')

doc = nlp('River encamina la renovación con Matías Suárez')
print(*[f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc.sentences for word in sent.words], sep='\n')