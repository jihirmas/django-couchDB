from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    country = models.CharField(max_length=100)
    description = models.TextField()

    def save(self, *args, **kwargs):
        from django.conf import settings
        db = settings.CLOUDANT['grupo10']
        doc = {
            'type': 'author',
            'name': self.name,
            'birth_date': self.birth_date.isoformat(),
            'country': self.country,
            'description': self.description
        }
        db.create_document(doc)
        super().save(*args, **kwargs)

class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    publication_date = models.DateField()
    sales = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        from django.conf import settings
        db = settings.CLOUDANT['grupo10']
        doc = {
            'type': 'book',
            'title': self.title,
            'summary': self.summary,
            'publication_date': self.publication_date.isoformat(),
            'sales': self.sales,
            'author_id': self.author.id
        }
        db.create_document(doc)
        super().save(*args, **kwargs)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review_text = models.TextField()
    score = models.IntegerField()
    up_votes = models.IntegerField()

    def save(self, *args, **kwargs):
        from django.conf import settings
        db = settings.CLOUDANT['grupo10']
        doc = {
            'type': 'review',
            'book_id': self.book.id,
            'review_text': self.review_text,
            'score': self.score,
            'up_votes': self.up_votes
        }
        db.create_document(doc)
        super().save(*args, **kwargs)

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    year = models.IntegerField()
    sales = models.IntegerField()

    def save(self, *args, **kwargs):
        from django.conf import settings
        db = settings.CLOUDANT['grupo10']
        doc = {
            'type': 'sale',
            'book_id': self.book.id,
            'year': self.year,
            'sales': self.sales
        }
        db.create_document(doc)
        super().save(*args, **kwargs)
