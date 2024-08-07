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
            sales = int(book['number_of_sales'])
            
            # Aggregate total sales for the author
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
