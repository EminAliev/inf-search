import re

from nltk.corpus import stopwords

pattern = re.compile("^[a-zA-Z]+$")
STOPWORDS = stopwords.words('russian')
