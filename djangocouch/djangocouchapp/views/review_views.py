from django.conf import settings
from django.shortcuts import render, redirect
import uuid
from django.core.cache import cache

my_database = settings.MY_DATABASE
SEARCH_ENGINE_ACTIVE = settings.SEARCH_ENGINE_ACTIVE
client_es = settings.CLIENT_ES
if client_es.ping() and client_es.indices.exists(index='reviews'):
    SEARCH_ENGINE_ACTIVE = True

def create_review(request):
    if request.method == "POST":
        book_id = request.POST.get('book')
        review = request.POST.get('review')
        score = request.POST.get('score')
        up_votes = request.POST.get('up_votes')
        data = {
            "_id": str(uuid.uuid4()),
            "book": book_id,
            "review": review,
            "score": score,
            "up_votes": up_votes,
            "type": "review",
        }
        my_database.create_document(data) 
    books = cache.get('books')
    if not books:
        books = [
            {'id': doc['id'], 'name': doc['doc']['name']} 
            for doc in my_database.all_docs(include_docs=True)['rows'] 
            if 'doc' in doc and doc['doc'].get('type') == 'book'
        ]
        cache.set('books', books, timeout=settings.CACHE_TTL)
    cache.delete('reviews_all')
    return render(request, 'review/create.html', {'books': books})

def edit_review(request, review_id):
    review = cache.get(f"review_{review_id}")
    if not review:
        review = my_database[review_id]
        cache.set(f"review_{review_id}", review, timeout=settings.CACHE_TTL)
    if request.method == "POST":
        
        book_id = request.POST.get('book')
        review_text = request.POST.get('review')
        score = request.POST.get('score')
        up_votes = request.POST.get('up_votes')
        
        
        review['book'] = book_id
        review['review'] = review_text
        review['score'] = score
        review['up_votes'] = up_votes
        my_database[review_id] = review  
        review.save() 
        cache.set(f"review_{review_id}", review, timeout=settings.CACHE_TTL)
        cache.delete('reviews_all')
        return redirect(f'/edit-review/{review_id}/')
    
    books = []
    for doc in my_database.all_docs(include_docs=True)['rows']:
        if 'doc' in doc and doc['doc'].get('type') == 'book' and doc['doc'].get('_id') != review['book']:
            books.append({'id': doc['id'], 'name': doc['doc']['name']})
        if 'doc' in doc and doc['doc'].get('type') == 'book' and doc['doc'].get('_id') == review['book']:
            book_name = doc['doc'].get('name')
    
    
    return render(request, 'review/edit.html', {'review': review, 'books': books, 'book_name': book_name, "review_id": review_id})

def delete_review(request, review_id):
    review = my_database[review_id]
    review.delete()
    cache.delete(f"review_{review_id}")
    cache.delete('reviews_all')
    return redirect('/list-reviews/')

def view_review(request, review_id):
    review = cache.get(f"review_{review_id}")
    if not review:
        review = my_database[review_id]
        cache.set(f"review_{review_id}", review, timeout=settings.CACHE_TTL)

    for doc in my_database.all_docs(include_docs=True)['rows']:
        if 'doc' in doc and doc['doc'].get('type') == 'book' and doc['doc'].get('_id') == review['book']:
            book_name = doc['doc'].get('name')
    
    return render(request, 'review/view.html', {'review': review, 'review_id': review['_id'], 'book_name': book_name})

def list_reviews(request):
    reviews = cache.get('reviews_all')
    if not reviews:
        reviews = []
        for doc in my_database.all_docs(include_docs=True)['rows']:
            if 'doc' in doc and doc['doc'].get('type') == 'review':
                reviews.append(doc)
        cache.set('reviews_all', reviews, timeout=settings.CACHE_TTL)
    return render(request, 'review/list_reviews.html', {'reviews': reviews})