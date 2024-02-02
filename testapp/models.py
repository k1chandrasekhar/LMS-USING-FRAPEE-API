from django.db import models

# Create your models here.


class Book(models.Model):
    name_of_book=models.CharField(max_length=500)
    name_of_author=models.CharField(max_length=500)
    Book_id=models.CharField(max_length=500)
    Curr_availability=models.IntegerField(default=0)
    isbn=models.CharField(max_length=500,default="##")
    publisher_name=models.CharField(max_length=500,default="None")
    PAGES_IN_BOOK=models.CharField(max_length=500,default="0")
    
    def __str__(self):
      return self.name_of_book

class Member(models.Model):
    user_name=models.CharField(max_length=500)
    name_of_member=models.CharField(max_length=500)
    name_of_book_issued=models.CharField(max_length=500)
    Book_id_issued=models.CharField(max_length=500)
    Date_of_book_issued=models.CharField(max_length=500)
    Date_of_return=models.CharField(max_length=500,default="NOT RETURNED")
    Paid_amount=models.IntegerField(default=0)

    def __str__(self):
      return self.name_of_book
    