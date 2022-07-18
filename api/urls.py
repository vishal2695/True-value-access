from django.urls import path
from . import views


urlpatterns = [

    path("signup/", views.signup, name="signup"),
    path("memberlist/", views.memberlist, name="memberlist"),
    path("addmember/", views.addmember, name="addmember"),
    path("updatemember/", views.updatemember, name="updatemember"),
    path("memberdetail/", views.memberdetail, name="memberdetail"),
    path("removemember/", views.removemember, name="removemember"),
    path("addbook/", views.addbook, name="addbook"),
    path("updatebook/", views.updatebook, name="updatebook"),
    path("removebook/", views.removebook, name="removebook"),
    path("booklistformember/", views.booklistformember, name="booklistformember"),
    path("borrowbook/", views.borrowbook, name="borrowbook"),
    path("returnbook/", views.returnbook, name="returnbook"),
    path("removeaccount/", views.removeaccount, name="removeaccount")



]