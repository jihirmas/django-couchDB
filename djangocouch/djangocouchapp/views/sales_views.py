from django.conf import settings
from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE


def list_sales(request):
    sales = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'sales'
    ]
    return render(request, 'sales/management.html', {'sales': sales})


def create_sale(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        sales = request.POST.get('sales')
        year = request.POST.get('year')

        data = {
            "_id": str(uuid.uuid4()),
            "book": book_id,
            "year": year,
            "sales": sales,
            "type": "sale"
        }
        my_database.create_document(data)

        
        return redirect('/sales_management/')

    books = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'book'
    ]
    return render(request, 'sales/create.html', {'books': books})


def edit_sale(request, sale_id):
    sale = my_database[sale_id]
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        sales = request.POST.get('sales')
        year = request.POST.get('year')

        sale['book'] = book_id
        sale['sales'] = sales
        sale["year"] = year
        my_database[sale_id] = sale  
        sale.save()
        
        return redirect('/sales_management/')

    books = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'book'
    ]
    return render(request, 'sales/edit.html', {'books': books, "sale": sale})


