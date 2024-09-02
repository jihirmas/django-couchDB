# book_views.py
from django.conf import settings
from django.shortcuts import render, redirect
import uuid
from django.core.cache import cache

my_database = settings.MY_DATABASE


def create_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author_id = request.POST.get('author')
        date_of_publication = request.POST.get('date_of_publication')
        summary = request.POST.get('summary')

        # Create and save a new book
        data = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "author": author_id,
            "date_of_publication": date_of_publication,
            "summary": summary,
            "type": "book"
        }
        my_database.create_document(data)

        # Redirect to the book management page
        return redirect('/book-management/')
 
    authors = cache.get('authors')
    if not authors:
        authors = [
            {'id': doc['id'], 'name': doc['doc']['name']} 
            for doc in my_database.all_docs(include_docs=True)['rows'] 
            if 'doc' in doc and doc['doc'].get('type') == 'author'
        ]
    
    return render(request, 'book/create.html', {'authors': authors})

def view_book(request, book_id):
    book = cache.get(f"book_{book_id}")
    if not book:
        book = my_database[book_id]
        cache.set(f"book_{book_id}", book, timeout=settings.CACHE_TTL)
    author = cache.get(f"author_{book_id}")
    if not author:
        author = my_database[book['author']]
        cache.set(f"author_{book_id}", author, timeout=settings.CACHE_TTL)
    return render(request, 'book/view.html', {'book': book, 'author': author})


def list_books(request):
    books = cache.get('books')
    if not books:
        books = [
            {'id': doc['id'], 'name': doc['doc']['name']} 
            for doc in my_database.all_docs(include_docs=True)['rows'] 
            if 'doc' in doc and doc['doc'].get('type') == 'book'
        ]
        cache.set('books', books, timeout=settings.CACHE_TTL)

    return render(request, 'book/management.html', {'books': books})


def edit_book(request, book_id):
    book = cache.get(f"book_{book_id}")
    if not book:
        book = my_database[book_id]
        cache.set(f"book_{book_id}", book, timeout=settings.CACHE_TTL)

    if request.method == "POST":
        name = request.POST.get('name')
        author_id = request.POST.get('author')
        date_of_publication = request.POST.get('date_of_publication')
        summary = request.POST.get('summary')
        
        book['name'] = name
        book['author'] = author_id
        book['date_of_publication'] = date_of_publication
        book['summary'] = summary
        my_database[book_id] = book
        book.save()
        cache.set(f"book_{book_id}", book, timeout=settings.CACHE_TTL)
        return redirect('book_management')
    
    authors = cache.get('authors')
    if not authors:
        authors = [
            {'id': doc['id'], 'name': doc['doc']['name']} 
            for doc in my_database.all_docs(include_docs=True)['rows'] 
            if 'doc' in doc and doc['doc'].get('type') == 'author'
        ]
        cache.set('authors', authors, timeout=settings.CACHE_TTL)

    return render(request, 'book/edit.html', {'book': book, 'authors': authors})

def delete_book(request, book_id):
    book = my_database[book_id]
    book.delete()
    cache.delete(f"book_{book_id}")
    return redirect('/list_books/')
