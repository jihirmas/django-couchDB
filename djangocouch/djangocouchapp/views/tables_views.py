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

    