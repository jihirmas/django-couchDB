from django.conf import settings
from django.shortcuts import render, redirect
import uuid

my_database = settings.MY_DATABASE

def list_sales(request):
    sales = []
    for doc in my_database.all_docs(include_docs=True)['rows']:
        if 'doc' in doc and doc['doc'].get('type') == 'sale':
            sale_id = doc['id']
            book_id = doc['doc']['book']
            # print(f"Attempting to fetch book with ID: {book_id}")  # Debugging line
            
            try:
                book_doc = my_database[book_id]
                # print(book_doc)

                if book_doc:
                    book_name = book_doc.get('name', 'Unknown Book')
                    # print(f"Fetched book: {book_doc}")  # Debugging line
                else:
                    book_name = 'Unknown Book'
                    # print(f"No document found for book ID: {book_id}")  # Debugging line
            except Exception as e:
                book_name = 'Unknown Book'
                # print(f"Error fetching book document for ID {book_id}: {e}")  # Debugging line
            
            sales.append({
                'id': sale_id,
                'book_name': book_name,
                'year': doc['doc'].get('year', 'Unknown Year'),
                'sales': doc['doc'].get('sales', 'Unknown Sales')
            })
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

        
        return redirect('/list-sales/')

    books = [
        {'id': doc['id'], 'name': doc['doc']['name']} 
        for doc in my_database.all_docs(include_docs=True)['rows'] 
        if 'doc' in doc and doc['doc'].get('type') == 'book'
    ]
    return render(request, 'sales/create.html', {'books': books})


def delete_sale(request, sale_id):
    sale = my_database[sale_id]
    sale.delete()
    return redirect('/list-sales/')


def edit_sale(request, sale_id):
    sale = my_database[sale_id]
    if request.method == "POST":
        sales = request.POST.get('sales')
        year = request.POST.get('year')

        sale['sales'] = sales
        sale["year"] = year
        my_database[sale_id] = sale  
        sale.save()
        
        return redirect('/list-sales/')

    return render(request, 'sales/edit.html', {"sale": sale})


