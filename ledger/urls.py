from django.urls import path, include
# from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from ledger import views
from pprint import pprint


router = routers.DefaultRouter()
router.register('creategroup', views.GroupListAndAddViewSet, basename='creategroup')
router.register('addexpenses', views.ExpenseReviewViewSet)

expense_router = routers.NestedDefaultRouter(router, 'addexpenses', lookup='expense')
expense_router.register('reviews', views.ExpenseReviewViewSet, basename='expense-reviews') # This is just a prefix of name to show.


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(expense_router.urls)),
    path('usercreatelist/', views.UserProfileListView.as_view()),
    path('creategroup', views.GroupListAndAddViewSet.as_view({'post': 'create'})),
    path('showdebts/', views.DebtsListView.as_view()),
    path('usertouserdebts/', views.DebtsUserToUser.as_view()),
    path('expenseuser/', views.ExpenseUsersApiView.as_view()),
    path('showexpenses/', views.ShowExpenseApiView.as_view()),
    path('addgroupexpense/', views.CreateExpenseApiView.as_view()),
    path('addexpenses/', views.AddExpensesApiView.as_view()),
    
]

    # For Group --->
    # path('grouplist/', views.GroupListView.as_view()),
    # path('newgroup/', views.AddUserToGroupApiView.as_view()),



