# Download data from Github
! git clone https://github.com/NetsecExplained/Machine-Learning-for-Security-Analysts.git
  
# Install dependencies
! pip install nltk sklearn pandas matplotlib seaborn
data_dir = "Machine-Learning-for-Security-Analysts/Malicious URLs.csv"

#_____________________________________________________________________________________________________________________________________________________#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import re

%matplotlib inline

# Import Scikit-learn helper functions
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# Import Scikit-learn models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

# Import Scikit-learn metric functions
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns

#_____________________________________________________________________________________________________________________________________________#

# Load the training data
print("- Loading CSV Data -")
url_df = pd.read_csv(data_dir)

test_url = url_df['URLs'][4]

# Let's see what our training data looks like
print(url_df)
#________________________________________________________________________________________________________________________________________________#
# Perform Train/Test split
test_percentage = .2
#________________________________________________________________________________________________________________________________________________#
train_df, test_df = train_test_split(url_df, test_size=test_percentage, random_state=42)

labels = train_df['Class']
test_labels = test_df['Class']

# Print counts of each class
print("- Counting Splits -")
print("Training Samples:", len(train_df))
print("Testing Samples:", len(test_df))
#_____________________________________________________________________________________________________________________________________________#
# Graph counts of each class, for both training and testing
count_train_classes = pd.value_counts(train_df['Class'])
count_train_classes.plot(kind='bar', fontsize=16)
plt.title("Class Count (Training)", fontsize=20)
plt.xticks(rotation='horizontal')
plt.xlabel("Class", fontsize=20)
plt.ylabel("Class Count", fontsize=20)

plt.show()
#______________________________________________________________________________________________________________________________________________#
count_test_classes = pd.value_counts(test_df['Class'])
count_test_classes.plot(kind='bar', fontsize=16, colormap='ocean')
plt.title("Class Count (Testing)", fontsize=20)
plt.xticks(rotation='horizontal')
plt.xlabel("Class", fontsize=20)
plt.ylabel("Class Count", fontsize=20)

plt.show()
#_______________________________________________________________________________________________________________________________________________#
# Define tokenizer
#   The purpose of a tokenizer is to separate the features from the raw data


def tokenizer(url):
  """Separates feature words from the raw data
  Keyword arguments:
    url ---- The full URL
    
  :Returns -- The tokenized words; returned as a list
  """
  
  # Split by slash (/) and dash (-)
  tokens = re.split('[/-]', url)
  
  for i in tokens:
    # Include the splits extensions and subdomains
    if i.find(".") >= 0:
      dot_split = i.split('.')
      
      # Remove .com and www. since they're too common
      if "com" in dot_split:
        dot_split.remove("com")
      if "www" in dot_split:
        dot_split.remove("www")
      
      tokens += dot_split
      
  return tokens
#_____________________________________________________________________________________________________________________________________________________#
# Let's see how our tokenizer changes our URLs

print("\n- Full URL -\n")
# (Write code here)
print(test_url)



# Tokenize test URL
print("\n- Tokenized Output -\n")
# (Write code here)
tokenized_url = tokenizer(test_url)
print(tokenized_url)
#__________________________________________________________________________________________________________________________________________________#
# Vectorizer the training inputs -- Takes about 30 seconds to complete
#   There are two types of vectors:
#     1. Count vectorizer
#     2. Term Frequency-Inverse Document Frequency (TF-IDF)

print("- Training Count Vectorizer -")
# (Write code here)
cVec = CountVectorizer(tokenizer= tokenizer)
count_X = cVec.fit_transform(train_df['URLs'])



print("- Training TF-IDF Vectorizer -")
# (Write code here)

tVec = TfidfVectorizer(tokenizer= tokenizer)
tfidf_X = tVec.fit_transform(train_df['URLs'])
#___________________________________________________________________________________________________________________________________________________#
# (Keep the following lines)
print("\n### Vectorizing Complete ###\n")

# Manually perform term count on test_url
# (Write code here)

for token in list(dict.fromkeys(tokenized_url)):
  print("{} - {}".format(tokenized_url.count(token),token))

print("\n- Count Vectorizer (Test URL) -\n")
# (Write code here)
exvec = CountVectorizer(tokenizer=tokenizer)
exx = exvec.fit_transform([test_url])
print(exx)
# (Keep the following lines)
print()
print("=" * 50)
print()

print("\n- TFIDF Vectorizer (Test URL) -\n")
# (Write code here)
exvec = TfidfVectorizer(tokenizer=tokenizer)
exx = exvec.fit_transform([test_url])
print(exx)
#________________________________________________________________________________________________________________________________________________#
# Vectorize the testing inputs
#   Use 'transform' instead of 'fit_transform' because we've already trained our vectorizers

print("- Count Vectorizer -")
# (Write code here)
test_count_X = cVec.transform(test_df['URLs'])



print("- TFIDF Vectorizer -")
# (Write code here)
test_count_X = tVec.transform(test_df['URLs'])

print("\n### Vectorizing Complete ###\n")
#________________________________________________________________________________________________________________________________________________#
# Define report generator

def generate_report(cmatrix, score, creport):
  """Generates and displays graphical reports
  Keyword arguments:
    cmatrix - Confusion matrix generated by the model
    score --- Score generated by the model
    creport - Classification Report generated by the model
    
  :Returns -- N/A
  """
  
  # Transform cmatrix because Sklearn has pred as columns and actual as rows.
  cmatrix = cmatrix.T
  #__________________________________________________________________________________________________________________________________________________#
  # Generate confusion matrix heatmap
  plt.figure(figsize=(5,5))
  sns.heatmap(cmatrix, 
              annot=True, 
              fmt="d", 
              linewidths=.5, 
              square = True, 
              cmap = 'Blues', 
              annot_kws={"size": 16}, 
              xticklabels=['bad', 'good'],
              yticklabels=['bad', 'good'])

  plt.xticks(rotation='horizontal', fontsize=16)
  plt.yticks(rotation='horizontal', fontsize=16)
  plt.xlabel('Actual Label', size=20);
  plt.ylabel('Predicted Label', size=20);

  title = 'Accuracy Score: {0:.4f}'.format(score)
  plt.title(title, size = 20);

  # Display classification report and confusion matrix
  print(creport)
  plt.show()
  

print("\n### Report Generator Defined ###\n")
#__________________________________________________________________________________________________________________________________________________#
# Multinomial Naive Bayesian with TF-IDF

# Train the model


mnb_tfidf = MultinomialNB()
mnb_tfidf.fit(tfidf_X, labels)

# Test the mode (score, predictions, confusion matrix, classification report)

score_mnb_tfidf = mnb_tfidf.score(test_count_X, test_labels)
predictions_mnb_tfidf = mnb_tfidf.predict(test_count_X)
cmatrix_mnb_tfidf = confusion_matrix(test_labels, predictions_mnb_tfidf)
creport_mnb_tfidf = classification_report(test_labels, predictions_mnb_tfidf)

# (Keep the following lines)
print("\n### Model Built ###\n")
generate_report(cmatrix_mnb_tfidf, score_mnb_tfidf, creport_mnb_tfidf)
#_________________________________________________________________________________________________________________________________________________#
# Logistic Regression with Count Vectorizer

# Train the model

lgs_tfidf = LogisticRegression(solver='lbfgs')
lgs_tfidf.fit(tfidf_X, labels)

# Test the mode (score, predictions, confusion matrix, classification report)
# (Write code here)
score_lgs_count = lgs_tfidf.score(test_count_X, test_labels)
predictions_lgs_tfidf = lgs_tfidf.predict(test_count_X)
creport_lgs_count = classification_report(test_labels, predictions_lgs_tfidf)
cmatrix_lgs_count = confusion_matrix(test_labels, predictions_lgs_tfidf)

# (Keep the following lines)
print("\n### Model Built ###\n")
generate_report(cmatrix_lgs_count, score_lgs_count, creport_lgs_count)
