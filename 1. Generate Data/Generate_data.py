import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Generate a list of dates from 2016-01-01 to today
start_date = datetime(2016, 1, 1)
end_date = datetime.now()
tags = ['Election', 'Football', 'Gadgets', 'COVID-19', 'Movies', 'Stock Market', 'Research']

def generate_dates(start_date, end_date):
    delta = end_date - start_date
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    return days

dates = generate_dates(start_date, end_date)

# Function to generate a single article
def generate_article(date):
    article = {
        'title': fake.sentence(nb_words=6),
        'author': fake.name(),
        'publication_date': date,
        'content': fake.paragraph(nb_sentences=10),
        'category': random.choice(['World', 'Technology', 'Sports', 'Business', 'Entertainment', 'Health','Politics', 'Technology', 'Science']),
    }
    return article

# Generate a list of articles
articles = []
for date in dates:
    # Random number of articles per day
    for _ in range(random.randint(1, 5)):
        articles.append(generate_article(date))

# Convert to DataFrame
df = pd.DataFrame(articles)

# Save to CSV (or any other format you prefer)
df.to_csv('dummy_news_articles.csv', index=False)
