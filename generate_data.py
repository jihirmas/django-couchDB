from faker import Faker
import uuid
from djangocouch.djangocouch.settings import MY_DATABASE
import random

fake = Faker()

# Generar varios autores
def create_authors(num_authors):
    authors = []
    for _ in range(num_authors):
        data = {
            "_id": str(uuid.uuid4()),
            "name": fake.name(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "country_of_origin": fake.country(),
            "description": fake.text(max_nb_chars=200),
            "type": "author"
        }
        authors.append(data)
        # Aquí es donde se llamaría a my_database.create_document(data)
        MY_DATABASE.create_document(data)
    return authors


def create_book(author_id):
    name = fake.sentence(nb_words=3)
    date_of_publication = fake.date()
    summary = fake.text()

    data = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "author": author_id,
        "date_of_publication": date_of_publication,
        "summary": summary,
        "type": "book"
    }
    MY_DATABASE.create_document(data)
    return data

def create_review(book_id):
    review = fake.text()
    score = random.randint(1, 5)
    up_votes = random.randint(0, 10000)
    
    data = {
        "_id": str(uuid.uuid4()),
        "book": book_id,
        "review": review,
        "score": score,
        "up_votes": up_votes
    }
    
    MY_DATABASE.create_document(data)
    return data


def create_sales(year_inicial, year_final, book):
    for year in range(year_inicial, year_final+1):
        data = {
            "book_id": book,
            "year": year,
            "sales": random.randint(1000, 100000)
        }
        MY_DATABASE.create_document(data)

# Por ejemplo, crear 10 autores
authors = create_authors(50)
for author in authors:
    for _ in range(6):
        book = create_book(author_id=author["_id"])
        n_reviews = random.randint(1,11)
        for _ in range(n_reviews):
            create_review(book["_id"])
        for year in range(random.randint(5,20)):
            year_final = 2024
            year_inicial = 2024 - year
            create_sales(year_inicial, year_final, book["_id"])
            



