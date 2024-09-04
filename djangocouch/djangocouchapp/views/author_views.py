from django.conf import settings
from django.shortcuts import render, redirect
import uuid
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage

my_database = settings.MY_DATABASE

def author_management(request):
    authors = cache.get('authors_all')
    if not authors:
        authors = [
            {
                'id': doc['id'], 
                'name': doc['doc']['name'], 
                'birth_date': doc['doc'].get('birth_date', '')
            } 
            for doc in my_database.all_docs(include_docs=True)['rows'] 
            if 'doc' in doc and doc['doc'].get('type') == 'author'
        ]
        cache.set('authors_all', authors, timeout=settings.CACHE_TTL)
    
    return render(request, 'author/management.html', {'authors': authors})

def create_author(request):
    if request.method == "POST":
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        country_of_origin = request.POST.get('country_of_origin')
        description= request.POST.get('description')

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)

        if request.FILES.get("file_url"): 
            image = request.FILES["file_url"]
            filename = fs.save(image.name,image)
            file_url = fs.url(filename)
        else:
            file_url = None

        data = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "birth_date": birth_date,
            "country_of_origin": country_of_origin,
            "description": description,
            "type": "author",
            "file_url": file_url
        }
        my_database.create_document(data)
        cache.delete('authors_all_data')
        cache.delete('authors_all')
        return redirect('author_management')
    return render(request, 'author/create.html')

def list_authors(request):
    authors = cache.get('authors_all_data')
    if not authors:
        authors = my_database.all_docs(include_docs=True)
        cache.set('authors_all_data', authors, timeout=settings.CACHE_TTL)
    return render(request, 'author/list.html', {'authors': authors})


def edit_author(request, author_id):
    author = cache.get(f"author_{author_id}")
    if not author:
        author = my_database[author_id]
        cache.set(f"author_{author_id}", author, timeout=settings.CACHE_TTL)
    if request.method == "POST":
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        country_of_origin = request.POST.get('country_of_origin')
        description = request.POST.get('description')
        print(f"Received name: {name}, birth_date: {birth_date}")
        
        author['name'] = name
        author['birth_date'] = birth_date
        author['country_of_origin'] = country_of_origin
        author['description'] = description
        my_database[author_id] = author  
        cache.set(f"author_{author_id}", author, timeout=settings.CACHE_TTL)
        author.save() #ojo que acá se guarda el documento no la bd para que funcione
        print(my_database[author_id])
        cache.delete('authors_all_data')
        cache.delete('authors_all')
        return redirect('author_management')
    return render(request, 'author/edit.html', {'author': author})

def delete_author(request, author_id):
    author = my_database[author_id]
    author.delete()
    cache.delete(f"author_{author_id}")
    cache.delete('authors_all_data')
    cache.delete('authors_all')
    return redirect('author_management')

def view_author(request, author_id):
    author = cache.get(f"author_{author_id}")
    if not author:
        author = my_database[author_id]
        cache.set(f"author_{author_id}", author, timeout=settings.CACHE_TTL)
    image_url = author.get("file_url", None)
    #print(image_url)
    return render(request, 'author/view.html', {'author': author,'cover_image_url': image_url})
