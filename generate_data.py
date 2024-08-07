from faker import Faker
import uuid
from djangocouch.djangocouch.settings import MY_DATABASE

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
            "description": fake.text(max_nb_chars=200)
        }
        authors.append(data)
        # Aquí es donde se llamaría a my_database.create_document(data)
        MY_DATABASE.create_document(data)
    return authors

# Por ejemplo, crear 10 autores
authors = create_authors(10)

# Imprimir los autores generados (solo para verificación)
for author in authors:
    print(author)
