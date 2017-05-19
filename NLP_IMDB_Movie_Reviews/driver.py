import csv
from itertools import cycle
import pandas as pd
import glob
import math as m
import string
import sys
import numpy as np
from sklearn.linear_model import SGDClassifier as SGD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer as tfidf

np.set_printoptions(threshold=np.nan)
train_path = "../aclImdb/train/" # source data
test_path = "../imdb_te.csv" # test data for grade evaluation. 
exclude = ['!','.',',','(',')','#','%','@','*',':',';','<','>','/','?','"',"'", "\n",'<br>',"<br />", "br", "-",'1','2','3','4','5','6','7','8','9','0']

def remove_punctuation(s):
	global exclude
	s = ''.join(ch for ch in s if ch not in exclude)
	return s 

def read_text_file(filepath):
	with open(filepath, "r") as f:
		data = f.read().replace('\n','')
	return data

def createIMDB(name):
	with open(name, "w") as train:
		neg_directory = "../aclImdb/train/neg/*.txt"		
		index=0
		for f in glob.glob(neg_directory):
			row = read_text_file(f) 
			s=str(index)+" , "+row+" , 0\n"
			train.write(s)
			index+=1
		pos_directory = "../aclImdb/train/pos/*.txt"		
		for f in glob.glob(pos_directory):	
			row = read_text_file(f) 
			s=str(index)+" , "+row+" , 1\n"
			train.write(s)
			index+=1

#Switched to CountVectorizer no longer needed Unigram/Bigram representation and their dictionaries
def create_Representations(stopwords, name):
	data = []
	#No longer need following arrays/dicts
	#unique_ds = []
	#bigram_ds = []
	#num_docs_per_word = {}
	#bi_num_docs_per_word = {}
	with open(name, "r") as orig:
		index=0
		for row in orig:
			data.append([])
			#unique_ds.append({})
			#bigram_ds.append({})	
	
			row = row.rsplit(',',1)
			row1 = row[0].split(',',1)
			newRow = [row1[0],row1[1],row[1].replace('\n','')]	
			words = newRow[1].lower().split()
			#new_set = set()
			for word in words:
				#Clean word
				new_word = remove_punctuation(word)
				#print(new_word)
				if word in stopwords or new_word in stopwords or word in exclude or new_word in exclude:
					#print("word: ", word)
					continue
				
				data[index].append(new_word)
				
				#Unigram Representation
				#Add to number of docs per word
				'''
				if new_word not in new_set:
					if new_word not in num_docs_per_word:
						num_docs_per_word[new_word]=1
						new_set.add(new_word)
					else:
						num_docs_per_word[new_word] = num_docs_per_word[new_word]+1
						new_set.add(new_word)

				if new_word not in unique_ds[index]:
					unique_ds[index][new_word] = 1
				else:
					num = unique_ds[index][new_word]
					num+=1
					unique_ds[index][new_word] = num
				'''
			#Bigram Representation
			'''
			licycle = cycle(data[index])
			nextelem = licycle.next()
			length = len(data[index])
			i=0
			new_set = set()
			while i<length:
				thisword, nextword = nextelem, licycle.next()
				combined_word = thisword+" "+nextword

				if combined_word not in new_set:
					if combined_word not in bi_num_docs_per_word:
						bi_num_docs_per_word[combined_word]=1
						new_set.add(combined_word)
					else:
						bi_num_docs_per_word[combined_word] = bi_num_docs_per_word[combined_word]+1
						new_set.add(combined_word)

				#print(combined_word)
				if combined_word in bigram_ds[index]:
					num = bigram_ds[index][combined_word]
					num+=1
					bigram_ds[index][combined_word]=num
				elif combined_word not in bigram_ds[index]:
					bigram_ds[index][combined_word] = 1 

				nextelem = nextword
				i+=1
			'''
			data[index].append(newRow[2])
			data[index].insert(0, newRow[0])
			index+=1
		return stopwords, data  #, unique_ds, bigram_ds, num_docs_per_word, bi_num_docs_per_word



def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
	temp = []
	with open("../stopwords.en.txt", "r") as stop:
		spamreader= csv.reader(stop)
		for row in spamreader:	
			temp.append(row)
	unravel = np.array(temp)
	stopwords = unravel.flatten()
	print("stopwords.en.txt...")	
	createIMDB(name)
	print("createIMDB...")
	return create_Representations(stopwords, name)

'''Implement this module to extract
and combine text files under train_path directory into 
imdb_tr.csv. Each text file in train_path should be stored 
as a row in imdb_tr.csv. And imdb_tr.csv should have three 
columns, "row_number", "text" and label'''


def termfrequency(number):
	num = 1+m.log(number)
	return num

def TF(ds):
	total = len(ds)
	x = 0
	for row in ds:
		for word in row:
			number = ds[x][word]
			logged_number = termfrequency(number)
			ds[x][word] = logged_number	
		x+=1

def TF_inverse(ds, num_docs_per_word):
	total = len(ds)
	x = 0
	for row in ds:
		for word in row:
			N = num_docs_per_word[word]
			number = ds[x][word]
			itf = inversetermfrequency(number, total, N)
			ds[x][word] = itf	
		x+=1

#tf-idf[t] = tf[t]*idf[t]
def inversetermfrequency(number, total, N):
	x = number * m.log(total/N)
	return x

def write_out(prediction, name):
	np.savetxt(name, prediction, fmt="%s")

	'''	
	with open(name, "w") as out:
		
		for x in np.nditer(prediction):
			s = str(x)+'\n'
			out.write(s)
		out.close()
	'''
if __name__ == "__main__":
	#No longer needed: unigram_ds, bigram_ds, num_docs_per_word, bi_num_docs_per_word 
	stopwords, data = imdb_data_preprocess(test_path)
	print("Data Collection Completed...") 

	labels = []
	for row in data:	
		s = row[len(row)-1].replace(' ','')
		labels.append(int(s))
	Y = np.asarray(labels)
	#Unsure from here down...
	print("Train Classifier...")	


	test = pd.read_csv(test_path)
	reviews = test[[1]]


	X_test = reviews['text'].tolist()
	for i in range(len(X_test)):
	    X_test[i] = ''.join(ch if ch.isalpha() else ' ' for ch in X_test[i].lower()) 
	    X_test[i] = ' '.join(word for word in (X_test[i].lower()).split() if word not in stopwords)



	X_train = []
	index = 0
	for row in range(len(data)):
		s=""
		for word in range(len(data[row])):		
			if word == len(data[row])-1 or word == 0:
				continue
			s += data[row][word]+" "
		X_train.append(s)

	'''train a SGD classifier using unigram representation, predict sentiments on imdb_te.csv, and write output to unigram.output.txt'''
	print("Unigram...")
	count_vector = CountVectorizer(ngram_range=(1,1))
	Z_train = count_vector.fit_transform(X_train)
	Z_test = count_vector.transform(X_test)

	clf = SGD(loss="hinge", penalty="l2")
	clf.fit(Z_train, Y)
	predict_unigram = clf.predict(Z_test)
	#print(predict_unigram)
	#exit()
	write_out(predict_unigram, "unigram.output.txt")	
	
	'''train a SGD classifier using bigram representation with tf-idf, predict sentiments on imdb_te.csv, and write output to unigram.output.txt'''
	print("Unigram tf-idf...")	

	Z_train = count_vector.fit_transform(X_train)
	Z_test = count_vector.transform(X_test)

	idf = tfidf(use_idf=True).fit(Z_train)
	Z_train = idf.transform(Z_train)
	Z_test = idf.transform(Z_test)
	
	clf = SGD(loss="hinge", penalty="l2")
	clf.fit(Z_train, Y)
	predict_unigram_tfidf = clf.predict(Z_test)
	#print(predict_unigram_tfidf)
	write_out(predict_unigram_tfidf, "unigramtfidf.output.txt")

	'''train a SGD classifier using bigram representation, predict sentiments on imdb_te.csv, and write output to unigram.output.txt'''
	print("Bigram...")
	count_vector_bi = CountVectorizer(ngram_range=(1,2))	
	Z_train = count_vector_bi.fit_transform(X_train)
	Z_test = count_vector_bi.transform(X_test)
	
	clf = SGD(loss="hinge", penalty="l2")
	clf.fit(Z_train, Y)
	predict_bigram = clf.predict(Z_test)
	write_out(predict_bigram, "bigram.output.txt")

	'''train a SGD classifier using unigram representation with tf-idf, predict sentiments on imdb_te.csv, and write output to unigram.output.txt'''

	print("Bigram tf-idf...")
	Z_train = count_vector_bi.fit_transform(X_train)
	Z_test = count_vector_bi.transform(X_test)
	
	bi_idf = tfidf(use_idf=True).fit(Z_train)
	Z_train = bi_idf.transform(Z_train)
	Z_test = bi_idf.transform(Z_test)
	
	clf = SGD(loss="hinge", penalty="l2")
	clf.fit(Z_train, Y)
	predict_bigram_tfidf = clf.predict(Z_test)
	write_out(predict_bigram_tfidf, "bigramtfidf.output.txt")
