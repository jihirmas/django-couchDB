# book_views.py
from django.conf import settings
from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE


def create_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author_id = request.POST.get('author')

        # Create and save a new book
        data = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "author": author_id,
            "type": "book"
        }
        my_database.create_document(data)

        # Redirect to the book management page
        return redirect('/')

    authors = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'author'
    ]
    print(f"Authors {authors}")
    return render(request, 'book/create.html', {'authors': authors})

def view_book(request, book_id):
    book = my_database[book_id]
    author = my_database[book['author']]
    return render(request, 'book/view.html', {'book': book, 'author': author})

def edit_book(request, book_id):
    book = my_database[book_id]
    if request.method == "POST":
        name = request.POST.get('name')
        author_id = request.POST.get('author')
        
        book['name'] = name
        book['author'] = author_id
        my_database[book_id] = book  
        book.save()
        
        return redirect('book_management')

    authors = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'author'
    ]
    return render(request, 'book/edit.html', {'book': book, 'authors': authors})

def delete_book(request, book_id):
    book = my_database[book_id]
    book.delete()
    return redirect('book_management')
