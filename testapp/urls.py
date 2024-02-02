from django.urls import path,include
# from .views import hello_world,add,create_user,get_user_by_name
from .views import working_on,import_book,go_home,find_book,issue_book,show_all_books,return_book,show_member

urlpatterns=[
    path("import",import_book,name="import"),
    path("return",return_book,name="return_book"),
    path("import_all",import_book,name="import"),
    path("member",show_member,name="show_member"),

    path("",go_home,name="empty"),
    path("show_all_books",show_all_books,name="show_all_books"),
    path("issue",issue_book,name="issue"),
    # path("",add_book,name="add_book"),
    path("go_home",go_home,name="go_home"),
    path("find",find_book,name="find"),

    # path("hello",hello_world,name="hello"),
    # path("add",add,name="add"),
    # path("add_user",create_user,name="add_user"),
    # path("search",get_user_by_name,name="search")
]