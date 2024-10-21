import pandas as pd
import tensorflow as tf
from transformers import BertTokenizer
import plotly.graph_objects as go
import plotly.express as px

class SentimentAnalyzer:
    def __init__(self):
        # Load Pre-trained BERT Tokenizer and Model
        self.tokenizer = BertTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        self.model = tf.keras.models.load_model('bert_sentiment_model.h5')  # Load the .h5 model

    # Function to preprocess text (batch processing)
    def preprocess_batch(self, texts):
        inputs = self.tokenizer(
            texts,
            max_length=512,
            truncation=True,
            padding=True,
            add_special_tokens=True,
            return_tensors='tf'  # Use TensorFlow tensors
        )
        return inputs

    # Function to predict sentiment (batch processing)
    def predict_sentiments(self, texts):
        inputs = self.preprocess_batch(texts)
        outputs = self.model(inputs)
        logits = outputs.logits
        predicted_classes = tf.argmax(logits, axis=1).numpy()

        # Map predicted classes to sentiments (0: Very Negative, 4: Very Positive)
        sentiment_map = {0: 'Very Negative', 1: 'Negative', 2: 'Neutral', 3: 'Positive', 4: 'Very Positive'}
        sentiments = [sentiment_map[pred] for pred in predicted_classes]
        return sentiments

    # Function to process the uploaded Excel or CSV file and extract reviews
    def process_file(self, file):
        # Check file extension
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            raise ValueError("Unsupported file format. Please upload an Excel (.xlsx) or CSV (.csv) file.")

        # Assuming the reviews are in a column named 'review_text' or 'product_rating'
        if 'review_text' in df.columns:
            reviews = df['review_text'].dropna().tolist()
        elif 'product_rating' in df.columns:
            reviews = df['product_rating'].dropna().tolist()
        else:
            raise ValueError("The file must have a 'review_text' or 'product_rating' column.")
        
        return reviews

    # Function to analyze reviews and provide summary
    def analyze_reviews(self, reviews):
        # Process reviews in batches for speed
        batch_size = 16
        sentiments = []
        positive_reviews = []
        negative_reviews = []

        for i in range(0, len(reviews), batch_size):
            batch_reviews = reviews[i:i+batch_size]
            batch_sentiments = self.predict_sentiments(batch_reviews)
            sentiments.extend(batch_sentiments)

            for review, sentiment in zip(batch_reviews, batch_sentiments):
                if 'Positive' in sentiment:
                    positive_reviews.append(review)
                elif 'Negative' in sentiment:
                    negative_reviews.append(review)

        sentiment_counts = pd.Series(sentiments).value_counts()
        return sentiment_counts, positive_reviews, negative_reviews

    # Function to create a plot for sentiment distribution
    def plot_sentiment_distribution(self, sentiment_counts):
        fig = go.Figure(data=[
            go.Bar(x=sentiment_counts.index, 
                   y=sentiment_counts.values,
                   marker=dict(color=px.colors.qualitative.Vivid),
                   text=sentiment_counts.values, 
                   textposition='outside')  # Display total count on top of each bar
        ])
        
        fig.update_layout(
            title="Sentiment Distribution",
            xaxis_title="Sentiment",
            yaxis_title="Count",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14),
            showlegend=False
        )
        
        return fig
