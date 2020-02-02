# Import data processing modules
from absl import logging
from tensorflow import keras
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

# Function to perform training and evaluation
def train_and_evaluate_with_module(hub_module, train_module=False):
  embedded_text_feature_column = hub.text_embedding_column(
      key="sentence", module_spec=hub_module, trainable=train_module)
  
  estimator = tf.estimator.DNNClassifier(
      hidden_units=[500, 100],
      feature_columns=[embedded_text_feature_column],
      n_classes=2,
      optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.003))
  
  estimator.train(input_fn=train_input_fn, steps=1000)
  train_eval_result = estimator.evaluate(input_fn=predict_train_input_fn)
  test_eval_result = estimator.evaluate(input_fn=predict_test_input_fn)
  
  training_set_accuracy = train_eval_result["accuracy"]
  test_set_accuracy = test_eval_result["accuracy"]
  
  return {"Training accuracy": training_set_accuracy, "Test accuracy": test_set_accuracy}, estimator

def create_model():
  # Import training dataset as a data frame.
  path = "NLP-master/train.csv"
  twitter_data = pd.read_csv(path)

  # Restructure data
  twitter_data = twitter_data.rename(columns = {"text":"sentence", "target":"polarity"})
  twitter_data = twitter_data.drop(columns = ["keyword", "location"])
  twitter_data = twitter_data.reindex(columns = ["sentence", "id", "polarity"])

  # Reduce logging output.
  logging.set_verbosity(logging.ERROR)

  # Split twitter data into train and test sets.
  num_tweets = twitter_data.shape[0]
  half_num_tweets = int(num_tweets / 2)
  train_df = twitter_data.head(half_num_tweets)
  test_df = twitter_data.tail(half_num_tweets)

  # Training input on the whole training set with no limit on training epochs.
  train_input_fn = tf.compat.v1.estimator.inputs.pandas_input_fn(
      train_df, train_df["polarity"], num_epochs=None, shuffle=True)

  # Prediction on the whole training set.
  predict_train_input_fn = tf.compat.v1.estimator.inputs.pandas_input_fn(
      train_df, train_df["polarity"], shuffle=False)

  # Prediction on the test set.
  predict_test_input_fn = tf.compat.v1.estimator.inputs.pandas_input_fn(
      test_df, test_df["polarity"], shuffle=False)

  # Train and evaluate the module
  [results, estimator] = train_and_evaluate_with_module("https://tfhub.dev/google/nnlm-en-dim128/1", True)
  print(results)
  # tweet_model = estimator.export_saved_model
  tweet_model = estimator
  return tweet_model

