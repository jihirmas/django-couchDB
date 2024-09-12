from django.shortcuts import render
from django.conf import settings
from django.core.cache import cache

my_database = settings.MY_DATABASE

try:
    SEARCH_ENGINE_ACTIVE = settings.SEARCH_ENGINE_ACTIVE
    client_es = settings.CLIENT_ES
    if client_es.ping() and client_es.indices.exists(index='reviews'):
        SEARCH_ENGINE_ACTIVE = True
except:
    SEARCH_ENGINE_ACTIVE = False

def get_top_50_books():
    books = []
    authors_sales = {}

    all_docs = cache.get('all_docs')
    if not all_docs:
        all_docs = my_database.all_docs(include_docs=True)['rows']
        cache.set('all_docs', all_docs, timeout=settings.CACHE_TTL)

    for doc in all_docs:
        if doc['doc'].get('type') == 'book':
            book = doc['doc']
            book_id = book['_id']
            book_name = book['name']
            author_id = book['author']
            year = book['date_of_publication'][:4]
            
            # Inicializar ventas del libro en 0
            sales = 0

            # Buscar documentos de tipo "sale" para calcular las ventas del libro
            for sale_doc in all_docs:
                if sale_doc['doc'].get('type') == 'sale' and sale_doc['doc'].get('book') == book_id:
                    sales += int(sale_doc['doc'].get('sales'))

            # Agregar ventas al autor
            if author_id in authors_sales:
                authors_sales[author_id] += sales
            else:
                authors_sales[author_id] = sales
            
            books.append({
                'book_id': book_id,
                'book_name': book_name,
                'author_id': author_id,
                'year': year,
                'sales': sales,
            })
    
    # Ordenar libros por ventas y obtener los 50 más vendidos
    top_books = sorted(books, key=lambda x: x['sales'], reverse=True)[:50]

    for book in top_books:
        year_books = [b for b in books if b['year'] == book['year']]
        year_books = sorted(year_books, key=lambda x: x['sales'], reverse=True)[:5]
        book['is_top_5'] = book in year_books
        book['author_sales'] = authors_sales[book['author_id']]

    return top_books

def top_50_books_view(request):
    top_books = get_top_50_books()
    return render(request, 'table/top_50.html', {'top_books': top_books})

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search_view(request):
    search_param = request.POST.get("search_param")
    books = []
    final_books = []
    print(f'esta activo: {SEARCH_ENGINE_ACTIVE}')
    print(search_param)
    if not SEARCH_ENGINE_ACTIVE:

        all_docs = cache.get('all_docs')
        if not all_docs:
            all_docs = my_database.all_docs(include_docs=True)['rows']
            cache.set('all_docs', all_docs, timeout=settings.CACHE_TTL)
            
        for doc in all_docs:
            if doc['doc'].get('type') == 'book':
                book = doc['doc']
                book_id = book['_id']
                book_name = book['name']
                book_summary = book["summary"]
                author_id = book['author']
                year = book['date_of_publication'][:4]
                

                
                books.append({
                    'id': book_id,
                    'name': book_name,
                    'author_id': author_id,
                    'year': year,
                    'book_summary' : book_summary
                })
        
        for book in books:
            if search_param in book['book_summary']:
                final_books.append(book)
            
            
    
    else:

        query = {
        "query": {
            "match": {
                "summary": search_param
            }
        }}
        
        
        response = client_es.search(index="books", body=query)
        
        # Mostrar los resultados
        for hit in response['hits']['hits']:
            final_books.append({
                'id': hit['_id'],
                'name': hit['_source']['name'],
                'author_id': hit['_source']['author'],
                'year': hit['_source']['date_of_publication'][:4],
                'book_summary': hit['_source']['summary'],
                })
    
    return render(request, 'table/search.html', {'books': final_books})

def get_top_10_rated_books():
    books = {}
    reviews = []

    all_docs = cache.get('all_docs')
    if not all_docs:
        all_docs = my_database.all_docs(include_docs=True)['rows']
        cache.set('all_docs', all_docs, timeout=settings.CACHE_TTL)

    # Recopilar todas las reseñas
    for doc in all_docs:
        if doc['doc'].get('type') == 'review':
            reviews.append(doc['doc'])
    
    # Agrupar las reseñas por libro y calcular las calificaciones promedio
    for review in reviews:
        book_id = review['book']
        score = int(review['score'])

        if book_id not in books:
            books[book_id] = {
                'total_score': 0,
                'review_count': 0,
                'highest_rated_review': review,
                'lowest_rated_review': review
            }
        
        books[book_id]['total_score'] += score
        books[book_id]['review_count'] += 1
        
        # Actualizar la reseña más alta
        if score > int(books[book_id]['highest_rated_review']['score']):
            books[book_id]['highest_rated_review'] = review

        # Actualizar la reseña más baja
        if score < int(books[book_id]['lowest_rated_review']['score']):
            books[book_id]['lowest_rated_review'] = review
    
    # Calcular la calificación promedio de cada libro
    for book_id, data in books.items():
        data['average_score'] = data['total_score'] / data['review_count']

    # Ordenar los libros por calificación promedio y obtener los 10 más calificados
    top_books = sorted(books.items(), key=lambda x: x[1]['average_score'], reverse=True)[:10]

    # Obtener detalles del libro y del autor
    result = []
    for book_id, data in top_books:
        book_doc = my_database[book_id]
        author_doc = my_database[book_doc['author']]

        result.append({
            'book_id': book_id,
            'book_name': book_doc['name'],
            'highest_rated_review': my_database[data['highest_rated_review']["_id"]]["review"],
            'lowest_rated_review': my_database[data['lowest_rated_review']["_id"]]["review"],
        })

    return result


def top_10_rated_books(request):
    top_books = get_top_10_rated_books()
    return render(request, 'table/top_10.html', {'top_books': top_books})


def get_author_statistics():
    authors = []
    books_by_author = {}
    sales_by_book = {}
    reviews_by_book = {}

    all_docs = cache.get('all_docs')
    if not all_docs:
        all_docs = my_database.all_docs(include_docs=True)['rows']
        cache.set('all_docs', all_docs, timeout=settings.CACHE_TTL)
    # Organizar los datos
    for doc in all_docs:
        if doc['doc'].get('type') == 'book':
            book = doc['doc']
            author_id = book['author']
            if author_id not in books_by_author:
                books_by_author[author_id] = []
            books_by_author[author_id].append(book)
        elif doc['doc'].get('type') == 'sale':
            sale = doc['doc']
            book_id = sale['book']
            if book_id not in sales_by_book:
                sales_by_book[book_id] = 0
            sales_by_book[book_id] += int(sale['sales'])
        elif doc['doc'].get('type') == 'review':
            review = doc['doc']
            book_id = review['book']
            if book_id not in reviews_by_book:
                reviews_by_book[book_id] = []
            reviews_by_book[book_id].append(int(review['score']))

    # Calcular estadísticas por autor
    for doc in all_docs:
        if doc['doc'].get('type') == 'author':
            author = doc['doc']
            author_id = author['_id']
            published_books = books_by_author.get(author_id, [])
            total_sales = sum(sales_by_book.get(book['_id'], 0) for book in published_books)
            all_scores = [score for book in published_books for score in reviews_by_book.get(book['_id'], [])]
            average_score = sum(all_scores) / len(all_scores) if all_scores else 0

            authors.append({
                'author_id': author_id,
                'author_name': author['name'],
                'number_of_books': len(published_books),
                'average_score': average_score,
                'total_sales': total_sales,
            })

    return authors

def author_statistics_view(request):
    authors = get_author_statistics()
    return render(request, 'table/author_stats.html', {'authors': authors})
