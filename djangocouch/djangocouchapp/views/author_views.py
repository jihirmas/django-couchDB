from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


my_database = settings.MY_DATABASE


def create_author(request):
    if request.method == "GET":
        return render(request, "author/create.html")
    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        
        # Create and save a new author
        data = {
            "id": 1,
            "name": name,
            "birth_date": birth_date
        }
        my_database.create_document(data)
        
        # Redirect to a success page or the home page
        return redirect('/')
    
    return render(request, 'create_author.html')

    
