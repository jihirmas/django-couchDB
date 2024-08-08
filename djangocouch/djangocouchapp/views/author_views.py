from django.conf import settings
from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE

def author_management(request):
    authors = [
        {
            'id': doc['id'], 
            'name': doc['doc']['name'], 
            'birth_date': doc['doc'].get('birth_date', '')
        } 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'author'
    ]
    return render(request, 'author/management.html', {'authors': authors})

def create_author(request):
    if request.method == "POST":
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        country_of_origin = request.POST.get('country_of_origin')
        description= request.POST.get('description')

        data = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "birth_date": birth_date,
            "country_of_origin": country_of_origin,
            "description": description,
            "type": "author"
        }
        my_database.create_document(data)

        return redirect('author_management')
    return render(request, 'author/create.html')

def list_authors(request):
    authors = my_database.all_docs(include_docs=True)
    return render(request, 'author/list.html', {'authors': authors})


def edit_author(request, author_id):
    author = my_database[author_id]
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
        author.save() #ojo que acá se guarda el documento no la bd para que funcione
        print(my_database[author_id])
        
        return redirect('author_management')
    return render(request, 'author/edit.html', {'author': author})

def delete_author(request, author_id):
    author = my_database[author_id]
    author.delete()
    return redirect('author_management')

def view_author(request, author_id):
    author = my_database[author_id]
    return render(request, 'author/view.html', {'author': author})
