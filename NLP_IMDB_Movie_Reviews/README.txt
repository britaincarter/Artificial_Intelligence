This program uses a Large Moview Review Dataset and is compiled from a collection of 50,000 reviews from IMDB on the condition that their are no more than 30 reviews per movie to predict if a movie review is positive or negative. From the training set negative reviews have a score equal to or less than 4 out 10. And positive reviews have a score of 7 or greater out of 10. Neutral reviews are not included in the dataset.

In this project I train a stochastic gradient descent classifier. This classifier is particularly handy for text data. I use the sklearn library to implement the SGD.

If you wish to download the data it is located at: http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz

To run the script simply enter in your terminal (compiled in python 2):

python driver.py

The driver.py references the dataset with the assumption you have downloaded the dataset from the above URL and placed it one directory above the driver. Also references a "stopwords.en.txt" a directory above which contains very common english words that are thrown out.

I created two different data representations to increase accuracy of the predicted moview reviews, specifically using unigram/bigram data representation. Here is a helpful link on n-grams: https://en.wikipedia.org/wiki/N-gram

Sometimes a high word count may not be meaningfull so to alleviate the issue i used term frequency:

tf[t] = 1 + log(f[t,d]) where f[t,d] is the count of term t in document d. Log dampens common words.

I also used inverse term frequency:

idf[t] = log(N/df[t]) where df[t] is the number of documents containing the term t and N is the total number of documents in the dataset.

Therefore, instead of just word frequency i combined the two for:

tf-idf[t] = tf[t] * idf[t]

Description of tf-idf: https://en.wikipedia.org/wiki/Tf-idf

The driver will output at run time the following files that contain the prediction of whether the respective review for the document is positive or negative. (0 for negative, 1 for positive)

unigram.output.txt
unigramfidf.output.txt
bigram.output.txt
bigramfidf.output.txt
