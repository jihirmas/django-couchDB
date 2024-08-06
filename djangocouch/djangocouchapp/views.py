
from django.conf import settings
from django.http import HttpResponse


my_database = settings.MY_DATABASE

data = {
    '_id': 'julia30', # Setting _id is optional
    'name': 'Julia',
    'age': 30,
    'pets': ['cat', 'dog', 'frog']
    }

def add_document(request):
    my_document = my_database.create_document(data)
    return HttpResponse("Any kind of HTML Here")  
    
def get_document(request, id):
    return HttpResponse(f'{my_database[id]}')
     

# def edit_document(request, id, dic):
#     my_document = my_database[id]

#     # Update the document content
#     # This can be done as you would any other dictionary
#     # my_document['name'] = 'Jules'
#     # my_document['age'] = 6
    
#     for key, value in dic.items():
#         my_document[key] = value
    
#     my_document.save()
    
# def delete_document(rquest, id):
#     my_document = my_database[id]
#     my_document.delete()