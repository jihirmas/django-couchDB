# book_views.py
from django.conf import settings

from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE
SEARCH_ENGINE_ACTIVE = settings.SEARCH_ENGINE_ACTIVE
client_es = settings.CLIENT_ES

if client_es.ping() and client_es.indices.exists(index='books'):
    SEARCH_ENGINE_ACTIVE = True

def create_book(request):
    if request.method == "POST":
        name = request.POST.get('name')
        author_id = request.POST.get('author')
        date_of_publication = request.POST.get('date_of_publication')
        summary = request.POST.get('summary')

        id_book = str(uuid.uuid4())
        data = {
            "_id": id_book,
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
        
        if SEARCH_ENGINE_ACTIVE:
            print('libro creado en SE')
            client_es.index(index='books',document=doc, id=id_book)

        my_database.create_document(data)

        # Redirect to the book management page
        return redirect('/book-management/')
 
    authors = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'author'
    ]
    
    return render(request, 'book/create.html', {'authors': authors})

def view_book(request, book_id):
    book = my_database[book_id]
    author = my_database[book['author']]
    return render(request, 'book/view.html', {'book': book, 'author': author})

def list_books(request):
    books = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'book'
    ]

    return render(request, 'book/management.html', {'books': books})


def edit_book(request, book_id):
    book = my_database[book_id]
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
        if SEARCH_ENGINE_ACTIVE:
            client_es.update(
                index='books',
                id=book_id,
                body={
                    'doc':{
                        'name': name,
                        'author': author_id,
                        'date_of_publication': date_of_publication,
                        'summary': summary,
                    }
                }
            )
            

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
    query = {
    "query": {
        "match_all": {}
        }
    }

    
    
    if SEARCH_ENGINE_ACTIVE:
        client_es.delete(index='books', id=book_id)
        
    return redirect('/list-books/')
