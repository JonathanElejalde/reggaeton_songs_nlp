# Detecting sexual content on reggaeton song lyrics

One of the biggest critics to reggaeton is the amount of sexual content in its lyrics and videos. So, I collected over 8500 reggaeton lyrics from [letras.com](https://www.letras.com/)
where the users upload them. Then, these lyrics were used to predict sexual content on the songs using weak supervision to label the data. Finally, 
I evaluated the different nlp models on a hand-labeled dataset with 600 songs.

## Steps

- [Scraping the data](https://github.com/JonathanElejalde/reggaeton_songs_nlp/tree/main/get_songs)    
requests - BeautifulSoup
- [Preprocessing](https://github.com/JonathanElejalde/reggaeton_songs_nlp/tree/main/preprocessing)       
Preprocessing was a big part of the project because a lot of the songs where upload using chat-language. This means, a lot of grammar and spelling errors.
  - [Text cleaning](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/preprocessing/text_cleaning_spelling.py)       
  Removes numbers, special characters, repeated paragraphs and lines.
  - [Spelling correction](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/preprocessing/spelling_correction.ipynb)
  - [Eliminate non-spanish lyrics](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/preprocessing/detect_language.py)
- [Labeling the songs](https://github.com/JonathanElejalde/reggaeton_songs_nlp/tree/main/label_songs)
  - [Hand-labeling](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/label_songs/label_songs.py)
  - [Weak supervision](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/label_songs/weak_supervision.ipynb)      
  I used snorkel for the weak supervision part
- [Training](https://github.com/JonathanElejalde/reggaeton_songs_nlp/tree/main/models)
  - [Bag of words](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/models/bag_of_words.ipynb)      
  Trained on naive bayes and logistic regression
  - [Bag of ngrams](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/models/bag_of_ngrams.ipynb)     
  Trained on naive bayes, logistic regression, SVM, and Gradient Boosting
- [Embeddings](https://github.com/JonathanElejalde/reggaeton_songs_nlp/tree/main/models)       
I tried pre-trained embeddings, however, they were not meaningful due to the nature of our task.
  - [Embeddings on the lyrics](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/models/training_word2vec.ipynb)       
  Using gensim word2vec model with cbow and skipgram techniques
  - [ML models on the lyrics embeddings](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/models/training_embeddings.ipynb)
  - [DL models using the lyrics embeddings](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/models/training_dl_models.ipynb)      
  Trained CNN, LSTM and GRU models.
  

## Scores
model                                         |  parameters                                                                                                                                           |  accuracy            |  recall
----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------
naive bayes - BoW                             |                                                                                                                                                       |  0.75 |  0.74
logistic regression - Bag of n-grams - tfidf  |  {'C': 1.0}                                                                                                                                           |  0.74 |  0.74
naive bayes - Bag of ngrams                   |                                                                                                                                                       |  0.77 |  0.74
naive bayes - Bag of ngrams - tfidf           |                                                                                                                                                       |  0.77  |  0.74
svm                                           |  {'C': 1.0}                                                                                                                                           |  0.73 |  0.75
Gradient Boosting on 120 svd scaled           |  {'n_estimators': 10, 'max_features': 'log2', 'max_depth': 15, 'learning_rate': 0.15, 'criterion': 'mae'}                                             |  0.72 |  0.73
Gradient Boosting on Tfidf                    |  {'criterion': 'friedman_mse', 'learning_rate': 0.025, 'max_depth': 10, 'max_features': 'log2', 'n_estimators': 10}                                   |  0.76  |  0.76
Gradient Boosting on cbow                     |  {'criterion': 'friedman_mse', 'learning_rate': 0.025, 'max_depth': 10, 'max_features': 'log2', 'n_estimators': 10}                                   |  0.76  |  0.76
Logistic regression on cbow                   |  {'C': 100.0, 'penalty': 'l2'}                                                                                                                        |  0.77  |  0.76
CNN on lyrics embeddings (word2vec - cbow)    |  {'optimizer': 'adam', 'Conv + pooling': 3, 'filters-size': (128, 5), 'batch_size': 256}                                                              |  0.74 |  0.74
LSTM on lyrics embeddings (word2vec - cbow)   |  {'optimizer': 'adam', 'LSTM layers - units': (1, 100), 'Dense layers - units': (2, 1024), 'Dropout rate after dense layers': 0.8, 'batch_size': 32}  |  0.74 |  0.74
GRU on lyrics embeddings (word2vec - cbow)    |  {'optimizer': 'adam', 'GRU layers - units': (2, 300), 'Dense layers - units': (2, 1024), 'Dropout rate after dense layers': 0.8, 'batch_size': 128}  |  0.74 |  0.74

## Improvements
As we can see, the scores could be better. These are some of the things that we can try:
- improve spelling correction
- improve the language detection. We still can find english words in the corpus
- add labeling functions using snorkel to identify non-sexual content
- check the errors and correct labels if necessary
- use active learning

## Wordcloud on sexual content lyrics
![Wordcloud on sexual content lyrics](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/sexual_content_wordcloud.png)

## Wordcloud on non-sexual content lyrics
![Wordcloud on non-sexual content lyrics](https://github.com/JonathanElejalde/reggaeton_songs_nlp/blob/main/no_sexual_content_wordcloud.png)



