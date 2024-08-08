from django.conf import settings
from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE

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
    books = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'book'
    ]
    
    return render(request, 'review/create.html', {'books': books})

def edit_review(request, review_id):
    review = my_database[review_id]
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
    return redirect('/create-review/')

def view_review(request, review_id):
    review = my_database[review_id]
    for doc in my_database.all_docs(include_docs=True)['rows']:
        if 'doc' in doc and doc['doc'].get('type') == 'book' and doc['doc'].get('_id') == review['book']:
            book_name = doc['doc'].get('name')
    
    return render(request, 'review/view.html', {'review': review, 'review_id': review['_id'], 'book_name': book_name})