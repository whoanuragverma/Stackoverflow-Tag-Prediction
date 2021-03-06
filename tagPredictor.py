# IMPORTING MODEL
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer


# READ DATA
df = pd.read_csv('data/output.csv')
import ast
df['tags'] = df['tags'].apply(lambda x: ast.literal_eval(x))

# Load from file
tagPredictorModel = joblib.load('tagPredictor.pkl')

tfidf = TfidfVectorizer(analyzer = 'word' , max_features=10000, ngram_range=(1,3) , stop_words='english')
X = tfidf.fit_transform(df['title'])

multilabel = MultiLabelBinarizer()
y = df['tags']
y = multilabel.fit_transform(y)

def getTags(question):
	question = tfidf.transform(question)
	tags = multilabel.inverse_transform(tagPredictorModel.predict(question))
	if len(tags[0]) == 0:
		return [['try rephrasing the question']]
	return tags
