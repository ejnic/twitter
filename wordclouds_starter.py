'''
In this workshop, we will generate three word clouds from a collection of tweets.
Each cloud will represent words from the data that are 'positive', 'negative',
and 'neutral'. We will guide you through creating the missing functions.

Any line starting with '#' is a comment and is there to explain code or give hints!
'''

#First we need to import all the libraries we need...
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud


'''
Below are two functions that will help us make the clouds.
'''
#This is a funtion we will write to filter words and get a more refined word cloud.
def FilterText(tweetblob):
	#This is the list of words to filter out:
	wordsToFilter = ['could', 'the', 'and', 'https','put','your','any', 'here', 'for','via', 'use',
					 'more', 'you', 'with', 'would', 'can', 'this', 'when', 'how',
					 'from','new','who','what', 'between', 'that', 'are', 'at', 'it', 'will',
					 'our', 'but']
	#This is a dictionary we'll fill with words that pass our filter:
	filteredDictionary = dict()

	#Now let's loop through and get rid of words we don't want. Some examples are included.
	for word in tweetblob.words:
		#skip tiny words
		if len(word) < 3:
			continue
		#skip words with random chars or numbers
		if not word.isalpha():
			continue
		#skip the words in the filter we created
		if word.lower() in wordsToFilter:
			continue

		#if the word meets all of our critera, add it to the filtered dictionary
		filteredDictionary[word.lower()] = tweetblob.word_counts[word.lower()]

	return filteredDictionary

#This is a function we will write to create a wordcloud with the data we have
def CreateCloud(filteredDictionary, plotnum, title):
	#use the Word Cloud library functions to create a word cloud with given parameters
	wordcloud = WordCloud(max_words=10).generate_from_frequencies(filteredDictionary)
	#use matplotlib functions to adjust how the graph looks
	plt.subplot(plotnum)
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.title(title)
	plt.axis("off")

	return wordcloud

'''
Below is the main code for this program. It will run automatically every time,
and we will use it to call the functions we write above.
'''
#Get the JSON data
tweetfile = open('tweets.json', 'r')
tweetdata = json.load(tweetfile)
tweetfile.close()

#Create lists for the each word cloud
positivewords = ''
negativewords = ''
neutralwords = ''

#Iterate through the text data; if the word matches the condition, add it to that list
for word in tweetdata:
	tweetblob = TextBlob(word['text'])
	if tweetblob.polarity > .7:
		positivewords += word['text']
	elif tweetblob.polarity < -.7:
		negativewords += word['text']
	else:
		neutralwords += word['text']


#Create text blobs from the lists.
positiveblob = TextBlob(positivewords)
negativeblob = TextBlob(negativewords)
neutralblob = TextBlob(neutralwords)



#Create a matplotlib figure
plt.figure(1)

#Create the three word clouds
CreateCloud(FilterText(negativeblob), 131, 'Negative Words')
#CreateCloud(FilterText(neutralblob), 131, 'Neutral Words')
#CreateCloud(FilterText(positiveblob), 131, 'Positive Words')

#Show the plot!
plt.show()
