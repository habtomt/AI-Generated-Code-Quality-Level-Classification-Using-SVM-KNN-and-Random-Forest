"""
Auto-generated Python code
Scenario : Content Moderation & Filtering
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.utils import shuffle
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter
from sklearn.metrics import f1_score
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from tensorboardX import SummaryWriter

# Define a custom dataset class for our data
class HateSpeechDataset(Dataset):
    def __init__(self, data, labels, tokenizer, max_len):
        self.data = data
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        text = self.data[item]
        label = self.labels[item]

        encoding = self.tokenizer.encode_plus(
            text,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# Define a custom model for our task
class HateSpeechModel(nn.Module):
    def __init__(self):
        super(HateSpeechModel, self).__init__()
        self.bert = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, 2)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        pooled_output = self.dropout(pooled_output)
        outputs = self.classifier(pooled_output)
        return outputs

# Load the dataset
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Prepare the data for training
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    return ' '.join(tokens)

train_data['text'] = train_data['text'].apply(preprocess_text)
test_data['text'] = test_data['text'].apply(preprocess_text)

# Split the data into training and validation sets
train_text, val_text, train_labels, val_labels = train_test_split(train_data['text'], train_data['label'], random_state=42, test_size=0.2, stratify=train_data['label'])

# Create a dataset class for our data
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
train_dataset = HateSpeechDataset(train_text.tolist(), train_labels.tolist(), tokenizer, max_len=512)
val_dataset = HateSpeechDataset(val_text.tolist(), val_labels.tolist(), tokenizer, max_len=512)

# Create data loaders for our datasets
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Initialize our model, optimizer, and loss function
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = HateSpeechModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-5)

# Train our model
for epoch in range(5):
    model.train()
    total_loss = 0
    for batch in train_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f'Epoch {epoch+1}, Loss: {total_loss / len(train_dataloader)}')
    model.eval()
    with torch.no_grad():
        total_correct = 0
        for batch in val_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = model(input_ids, attention_mask)
            _, predicted = torch.max(outputs.scores, dim=1)
            total_correct += (predicted == labels).sum().item()
        accuracy = total_correct / len(val_labels)
        print(f'Epoch {epoch+1}, Val Accuracy: {accuracy:.4f}')

# Evaluate our model on the test set
test_dataset = HateSpeechDataset(test_data['text'].tolist(), test_data['label'].tolist(), tokenizer, max_len=512)
test_dataloader = DataLoader(test_dataset, batch_size=32, shuffle=False)
model.eval()
with torch.no_grad():
    total_correct = 0
    for batch in test_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask)
        _, predicted = torch.max(outputs.scores, dim=1)
        total_correct += (predicted == labels).sum().item()
    accuracy = total_correct / len(test_labels)
    print(f'Test Accuracy: {accuracy:.4f}')

# Use the model to flag content for review
def flag_content(text):
    input_ids = tokenizer.encode_plus(
        text,
        max_length=512,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt',
    )
    input_ids = input_ids['input_ids'].to(device)
    attention_mask = input_ids['attention_mask'].to(device)
    outputs = model(input_ids, attention_mask)
    _, predicted = torch.max(outputs.scores, dim=1)
    return predicted.item()

# Example usage:
text = "This is a sample text that contains hate speech."
flag = flag_content(text)
if flag == 1:
    print("Content flagged for review")
else:
    print("Content does not contain hate speech")