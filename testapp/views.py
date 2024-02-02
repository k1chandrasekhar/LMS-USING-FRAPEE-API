from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db import transaction
from datetime import datetime
from django.contrib import messages
import requests
# Create your views here.
from .models import Book,Member
from datetime import datetime
date_format = "%Y-%m-%d"







def show_all_books(request):
     book_obj=Book.objects.all()
     book_list = list(book_obj.values())
     context = {
        "books": book_list,  
    }
     return render(request,"Show_all_books.html",context)

def return_book(request):
     if request.method=="POST":
        name_member=request.POST.get("Name of Member")
        book_name=request.POST.get("Name of Book")
        Date_of_book_return=request.POST.get("RETURN DATE")
        book_id=request.POST.get("BOOK ID")
        unique_name=request.POST.get("USER NAME")
        Member_obj=Member()
        try:
             Member_obj=Member.objects.get(user_name=unique_name,name_of_member=name_member,name_of_book_issued=book_name)
        except Member.DoesNotExist:
             return HttpResponse("PLEASE ENTER CORRECT INFORMATION")     
        Date_of_issue=Member_obj.Date_of_book_issued
        try:
            per_day_charge=10
            book_object=Book()
            book_obj=Book.objects.get(Book_id=book_id, name_of_book=book_name)
            if Member_obj.Paid_amount!=0:
                 return HttpResponse("BOOK ALREADY RETURNED")
            start_date = datetime.strptime(Date_of_issue, "%Y-%m-%d").date()
            end_date = datetime.strptime(Date_of_book_return, "%Y-%m-%d").date()
            book_obj.Curr_availability+=1
            book_obj.save()
            Member_obj.Date_of_return=Date_of_book_return
            days_difference = (end_date - start_date).days
            days_difference=int(days_difference)
            print("days difference:", days_difference)
            amount=days_difference*per_day_charge
            Member_obj.Paid_amount=amount
            Member_obj.save()
            print("try accept")
            
            
                
            return HttpResponse("BOOK RETURNED SUCCESSFULLY THE TOTAL PRICE FOR LENDING BOOK:  "+str(amount))     
        except Book.DoesNotExist:
             return HttpResponse("PLEASE ENTER CORRECT INFORMATION")         
     return render(request,"RETURN.html")
    


def show_member(request):
     member_obj=Member.objects.all()
     member_list = list(member_obj.values())
     context = {
        "members": member_list,  
    }
     return render(request,"Show_member_list.html",context)

def issue_book(request):
    if request.method=="POST":
        name_member=request.POST.get("member_name")
        book_name=request.POST.get("book_name")
        Date_of_issue=request.POST.get("issue_date")
        book_id=request.POST.get("book_id")
        unique_name=request.POST.get("user_name")
        print(book_name,book_id)
        mem_obj=Member.objects.filter(user_name=unique_name)
        if mem_obj.exists():
             return HttpResponse("USER NAME ALREADY IN USE")
        
        try:
            
            print("trying")
            book_object=Book.objects.get(Book_id=book_id, name_of_book=book_name)
            print("execption")
            print("try accept")
            
            
                      
            if book_object.Curr_availability==0:
                        print("nOt avaialable")
                        return HttpResponse("BOOK  NOT AVAILABLE")
            else:
                 print(book_object.Book_id,book_object.name_of_book)
                 print("BOOK available")
                 book_object.Curr_availability-=1
                 book_object.save()
                 Member.objects.create(name_of_member=name_member,name_of_book_issued=book_name,Date_of_book_issued=Date_of_issue,Book_id_issued=book_id,user_name=unique_name)
                 return HttpResponse("BOOK  ISSUED SUCCESSSFULLY  THE ID TO RETURN THE BOOK IS "+"( "+unique_name +" )"+" PLEASE REMMEMBER IT")
                 
            
        except Book.DoesNotExist:
            return HttpResponse("NO BOOK IN RECORD")
        
        
    return render(request,"ISSUE_BOOK.html")



def working_on(request):
    return render(request,"viewbooks.html")


def import_book(request):
   
    
    if request.method=="POST":
        
         
         if "title" in request.POST and "author" in request.POST:
               print("box func")
               book_name=request.POST.get("title")
               author_name=request.POST.get("author")
               Number_of_books=int(request.POST.get("number_of_books"))
               url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
               response = requests.get(url)
               if response.status_code == 200:
                    content = response.json()
                    all_books = content.get("message", [])
                    with transaction.atomic():
                        try:
                             flag=True
                             for product in all_books:
                                  if(product.get("title")==book_name and product.get("authors")==author_name):
                                       print("added")
                                       var=product.get("  num_pages")
                                       print(var)
                                       flag=False
                                       book_obj=Book.objects.filter(Book_id=product.get("bookID"))
                                       
                                       if book_obj.exists():
                                            book_object=Book.objects.get(Book_id=product.get("bookID"))
                                            a=int(book_object.Curr_availability)
                                            b=int(Number_of_books)
                                            print(a)
                                            print(b)
                                            
                                            print(a+b)
                                            c=a+b
                                            book_object.Curr_availability=c
                                            # book_obj.Curr_availability+=Number_of_books
                                            book_object.save()
                                             
                                            return HttpResponse("BOOKS IMPORTED SUCCESSFULLY")
                                            
                                       else:
                                            Book.objects.create(name_of_book=product.get("title"), name_of_author=product.get("authors"),Book_id=product.get("bookID"),Curr_availability=Number_of_books,isbn=product.get("isbn"),publisher_name=product.get("publisher"),PAGES_IN_BOOK=int(var))
                                            
                                            return HttpResponse("BOOKS IMPORTED SUCCESSFULLY")
                                            
                                                          
                             if flag==True:
                                       return HttpResponse("BOOK DOES NOT EXIST IN API")
                        except Book.DoesNotExist:
                                  return HttpResponse("BOOK DOES NOT EXIST IN API")     
                          
         else:
              print("this is post")
            #   print("this is get")
              url = "https://frappe.io/api/method/frappe-library?page=2&title=and"
              response = requests.get(url)
              Number_of_books=request.POST.get("number_of_books")
              if response.status_code == 200:
                   content = response.json()
                   all_books = content.get("message", [])
                   with transaction.atomic():
                         
                               for product in all_books:
                                     print(product.get("title"))
                                     var=product.get("  num_pages")
                                     print(var)
                                     book_obj=Book.objects.filter(Book_id=product.get("bookID"))

                                     
                                     if book_obj.exists():
                                            book_object=Book.objects.get(Book_id=product.get("bookID"))
                                            a=int(book_object.Curr_availability)
                                            b=int(Number_of_books)
                                            print(a)
                                            print(b)
                                            c=a+b
                                            book_object.Curr_availability=c
                                            print(a+b)
                                            # book_object.Curr_availability+=Number_of_books
                                            book_object.save()
                                            
                                     else:
                                            print("going here")
                                            Book.objects.create(name_of_book=product.get("title"), name_of_author=product.get("authors"),Book_id=product.get("bookID"),Curr_availability=Number_of_books,isbn=product.get("isbn"),publisher_name=product.get("publisher"),PAGES_IN_BOOK=int(var))
                                            
         return HttpResponse("BOOKS IMPORTED SUCCESSFULLY")
                         
                              
                   
                              
                              
              
    return render(request, 'IMPORT_BOOKS.html')
         

                           
    
         
                 
                         



    # Checkining if the API call was successful
    
    
    
    
def go_home(request):
    
    return render(request,"viewbooks.html")


def find_book(request):
    
    if request.method == "GET":
        return render(request, "Find_book.html")

    book_name = request.POST.get("title")
    author_name = request.POST.get("author")
    
    if not book_name and not author_name:
        return HttpResponse("PLEASE PROVIDE AT LEAST ONE FIELD")

    book_list = []
    
    if book_name and not author_name:
        try:
            book_obj = Book.objects.get(name_of_book=book_name)
            book_list.append(book_obj)
        except Book.DoesNotExist:
            return HttpResponse("BOOK NOT IN RECORD")
    elif author_name and not book_name:
        try:
            book_obj = Book.objects.get(name_of_author=author_name)
            book_list = list(Book.objects.filter(name_of_author=author_name).values())
        except Book.DoesNotExist:
            return HttpResponse("BOOK NOT IN RECORD")
    else:
        try:
            book_list = list(Book.objects.filter(name_of_book=book_name, name_of_author=author_name).values())
            if not book_list:
                return HttpResponse("BOOK NOT IN RECORD")
        except Book.DoesNotExist:
            return HttpResponse("BOOK NOT IN RECORD")

    context = {
        "books": book_list,
    }
    return render(request, "Show_data.html", context)
              
   
