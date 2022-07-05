from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from ledger import views
from pprint import pprint


router = DefaultRouter()
router.register('creategroup', views.GroupListAndAddViewSet)


urlpatterns = [
    path('usercreatelist/', views.UserProfileListView.as_view()),
    path('groups/', include(router.urls)),
    # path('grouplist/', views.GroupListView.as_view()),
    # path('newgroup/', views.AddUserToGroupApiView.as_view()),
    path('showdebts/', views.DebtsListView.as_view()),
    path('usertouserdebts/', views.DebtsUserToUser.as_view()),
    path('expenseuser/', views.ExpenseUsersApiView.as_view()),
    path('showexpenses/', views.ShowExpenseApiView.as_view()),
    path('addgroupexpense/', views.CreateExpenseApiView.as_view()),
    path('addexpenses/', views.AddExpensesApiView.as_view())  
]





