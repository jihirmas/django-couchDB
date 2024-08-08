from django.shortcuts import render
from django.conf import settings

my_database = settings.MY_DATABASE

def get_top_50_books():
    books = []
    authors_sales = {}

    all_docs = my_database.all_docs(include_docs=True)['rows']

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


def search_view(request):
    search_param = request.POST.get("search_param")
    books = []

    all_docs = my_database.all_docs(include_docs=True)['rows']

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
    final_books = []
    for book in books:
        if search_param in book['book_summary']:
            final_books.append(book)
    
    return render(request, 'table/search.html', {'books': final_books})

def get_top_10_rated_books():
    books = {}
    reviews = []

    all_docs = my_database.all_docs(include_docs=True)['rows']

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
    print(top_books)
    return render(request, 'table/top_10.html', {'top_books': top_books})
