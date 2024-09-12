from faker import Faker
import uuid
from djangocouch.settings import MY_DATABASE
import random
from cloudant.client import CouchDB
from elasticsearch import Elasticsearch
fake = Faker()
database_name = 'grupo10'

client = CouchDB("admin", "admin", url='http://my-couchdb:5984', connect=True)
if database_name in client:
    MY_DATABASE = client[database_name]
else:
    MY_DATABASE = client.create_database('grupo10')

try:
    SEARCH_ENGINE_ACTIVE = False
    client_es = Elasticsearch(
        ["https://my-elasticsearch:9200"],  
        http_auth=("elastic", "admin"),                           
        verify_certs=False,
    )
    mappings_books = {
        'properties':{
            'name': {'type': 'text'},
            'author': {'type': 'text'},
            'date_of_publication': {'type': 'text'},
            'summary': {'type': 'text'},
            'type': {'type': 'text'},
        }
    }
    mappings_reviews = {
        'properties':{
            'book': {'type': 'text'},
            'review': {'type': 'text'},
            'score': {'type': 'integer'},
            'up_votes': {'type': 'integer'},
            'type': {'type': 'text'},
        }
    }
    if not client_es.indices.exists(index='books') and client_es.ping():
        client_es.indices.create(index='books', mappings=mappings_books)
        SEARCH_ENGINE_ACTIVE = True
        print("Index 'books' created successfully.")
    else:
        print("Index 'books' already exists.")


    if not client_es.indices.exists(index='reviews') and client_es.ping():
        client_es.indices.create(index='reviews', mappings=mappings_reviews)
        SEARCH_ENGINE_ACTIVE = True
        print('Index reviews CREATED')
    else:
        print('Index reviews already EXISTS')
except:
    SEARCH_ENGINE_ACTIVE = False
# Generar varios autores
def create_authors(num_authors):
    authors = []
    for n in range(num_authors):
        print(f"author {n}")
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
    id_asociado=str(uuid.uuid4())
    data = {
        "_id": id_asociado,
        "name": name,
        "author": author_id,
        "date_of_publication": date_of_publication,
        "summary": summary,
        "type": "book"
    }

    doc = {
        "name": name,
        "author": author_id,
        "date_of_publication": date_of_publication,
        "summary": summary,
        "type": "book"
    }
    try:
        client_es.index(index='books',document=doc, id=id_asociado)
    except:
        pass
    MY_DATABASE.create_document(data)
    return data

def create_review(book_id):
    review = fake.text()
    score = random.randint(1, 5)
    up_votes = random.randint(-10000, 10000)
    id_asociado = str(uuid.uuid4())
    data = {
        "_id": id_asociado,
        "book": book_id,
        "review": review,
        "score": score,
        "up_votes": up_votes,
        "type": "review"
    }

    doc = {
        "book": book_id,
        "review": review,
        "score": score,
        "up_votes": up_votes,
        "type": "review"
    }
    try:
        client_es.index(index='reviews',document=doc, id=id_asociado)
    except:
        pass
    MY_DATABASE.create_document(data)
    return data


def create_sales(year_inicial, year_final, book):
    for year in range(year_inicial, year_final+1):
        data = {
            "book": book,
            "year": year,
            "sales": random.randint(1000, 100000),
            "type": "sale"
        }
        MY_DATABASE.create_document(data)

# Por ejemplo, crear 10 autores
authors = create_authors(3)
for i, author in enumerate(authors):
    for n in range(2):
        book = create_book(author_id=author["_id"])
        print(f"creating book {n*i + n}")
        n_reviews = random.randint(1,11)
        for _ in range(n_reviews):
            create_review(book["_id"])
        for year in range(random.randint(5,20)):
            year_final = 2024
            year_inicial = 2024 - year
            create_sales(year_inicial, year_final, book["_id"])
        print("ready book")



