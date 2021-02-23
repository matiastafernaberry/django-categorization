from nltk import word_tokenize
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('spanish')
a = stemmer.stem('River')
print(a)