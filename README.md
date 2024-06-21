# Asterisk Machine Learning
Machine Learning related stuff for Asterisk, a mobile-based application for sentiment analysis focused on restaurants, cafes, and similar establishments.

## Dataset
We made [our own custom-made dataset](https://github.com/dennyrianto/asterisk-machine-learning/blob/main/data/dataset_final.parquet), which was combined from two public dataset:

https://www.kaggle.com/datasets/joebeachcapital/restaurant-reviews
https://huggingface.co/datasets/mrcaelumn/yelp_restaurant_review_labelled

## Data Preprocessing
For the preprocessing step, we labelled our dataset with multiple label using a [Python script](data/label.py).

## Model
For the model architecture, we fine-tuned a pre-trained transformers model (DistilBERT) and we added our own layers. We trained the model using our custom-made dataset. The model generates multiple outputs corresponding to different aspects of sentiment. Then we converted our model to Tensorflow.js format for deployment.

- [Model File (SavedModel Format)](https://drive.google.com/file/d/1iu_hIZLIFaDeruR8wB_3Cwn-gv5IgKEw/view?usp=drive_link)

- [Model File (TensorFlow.js Format)](https://drive.google.com/file/d/1pTHeiF0aSyyEazbTv2VPUz_h5htPLJGp/view?usp=drive_link)

