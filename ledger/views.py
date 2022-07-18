from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework_xml.renderers import XMLRenderer
from ledger.serializers import AddExpenseSerializer, DebtSerializer, ExpenseReviewSerializer, GroupSerializer, UserProfileSerializer, ExpenseUserSerializer, ExpenseSerializer
from ledger.models import ExpenseReview, UserProfileManager, UserProfile, Expense, ExpenseUser, Group, Debt, AddExpense
from rest_framework.views import APIView



class UserProfileListView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['email', 'name']


    # def get_queryset(self):              # This method is useful when we have some logic , some conditions etc.
    #     return UserProfile.objects.all() # Watch the commented get_queryset in GroupListAndAddViewSet
    # def get_serializer_class(self):
    #     return UserProfileSerializer     # This method is useful when we have some logic ,prehaps some different users or roles or different serializer classes.

    def create(self, request) -> Response:
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        name = serializer.validated_data.get('name')
        return Response({'message': f'User {name} created successfully'})

        


# class UserProfileListView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """

#     def get(self, request, format=None):
#         users = UserProfile.objects.all()                    # User objects thats are created.
#         serializer = UserProfileSerializer(users, many=True) # many is given to get many objects thats are passed. 
#         return Response(serializer.data)                     # many = False, gives only a single object.


# class UserProfileApiView(APIView):
#     # """
#     # List all snippets, or create a new snippet.
#     # """

#     """Test API View"""
#     serializer_class = UserProfileSerializer

#     def post(self, request) -> Response:
#         """Create a hello message with our name"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         name = serializer.validated_data.get('name')
#         return Response({'message': f'User {name} created successfully'})


class GroupListAndAddViewSet(ModelViewSet):
    """
    List all groups, or create a new group.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['debts', 'members']
    search_fields = ['group_name', 'members__name']
    ordering_fields = ['group_name', 'members__name']
    pagination_class = PageNumberPagination
    # renderer_classes = [XMLRenderer, ]
    http_method_names = ['post', 'get']

    def get_queryset(self):
        queryset =  Group.objects.all()
        debts_id = self.request.query_params.get('debts_id')
        if debts_id is not None:
            queryset = queryset.filter(debts_id=debts_id)
        return queryset

    def list(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = {
            "group_name": request.POST.get('group_name', None),
            "debts": request.POST.get('debts', None),
            "members": request.POST.get('members', None),
        }
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            group = Group.objects.create(group_name=data.get('group_name'))
            print(group)

            group_name = request.data.get('group_name')
            members = request.data.get('members')
            debt = request.data.get('debts')
            print(members)
            print(group_name)

            groups = Group.objects.get(group_name=group_name)
            print(groups)

            if members:
                for member in members:
                    user = UserProfile.objects.get(id=member)
                    if not groups.members.filter(id=user.id).exists():
                        groups.members.add(user)


            return Response({"status": "Group Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GroupListView(APIView):
#     """
#     List all groups, or create a new group.
#     """

#     def get(self, request, format=None):
#         groups = Group.objects.all()
#         serializer = GroupSerializer(groups, many=True)
#         return Response(serializer.data)


# class AddUserToGroupApiView(APIView):
#     """ Create a hello message with our name """

#     def post(self, request):
#         # import ipdb
#         # ipdb.set_trace()
#         serializer = GroupSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.validated_raise_exception=Truedata
#             group = Group.objects.create(group_name=data.get('group_name'))
#             print(group)

#             group_name = request.data.get('group_name')
#             members = request.data.get('members')
#             debt = request.data.get('debts')
#             print(members)
#             print(group_name)

#             groups = Group.objects.get(group_name=group_name)
#             print(groups)

#             if members:
#                 for member in members:
#                     user = UserProfile.objects.get(id=member)
#                     if not groups.members.filter(id=user.id).exists():
#                         groups.members.add(user)


#             return Response({"status": "Group Created"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtsListView(APIView):
    """
    List all debts or newly created.
    """

    def get(self, request, format=None):
        debts = Debt.objects.all()
        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data)


class DebtsUserToUser(APIView):
    def post(self, request):
        serializer = DebtSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # print(data)

            from_user = request.data.get('from_user')
            to_user = request.data.get('to_user')
            newamount = request.data.get('amount')
            # print(from_user)
            # print(to_user)
            # print(newamount)

            """ Method 1 """
            # Debt.objects.create(from_user_id=from_user, to_user_id=to_user, amount=newamount)

            """ Method 2 """
            from_user_obj = UserProfile.objects.get(id=from_user)
            to_user_obj = UserProfile.objects.get(id=to_user)

            Debt.objects.create(from_user=from_user_obj,
                                to_user=to_user_obj, amount=newamount)

            return Response({"status": "Debts Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseUsersApiView(APIView):
    def post(self, request):
        serializer = ExpenseUserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)

            user = request.data.get('user')
            paid_share_obj = request.data.get('paid_share')
            owed_share_obj = request.data.get('owed_share')
            net_balance_obj = request.data.get('net_balance')
            print(user)
            print(paid_share_obj)
            print(owed_share_obj)
            print(net_balance_obj)

            """ Method 1 """
            # ExpenseUser.objects.create(user_id=user, paid_share=paid_share_obj, owed_share=owed_share_obj, net_balance=net_balance_obj)

            """ Method 2 """
            user_obj = UserProfile.objects.get(id=user)
            ExpenseUser.objects.create(
                user=user_obj, paid_share=paid_share_obj, owed_share=owed_share_obj, net_balance=net_balance_obj)

            return Response({"status": "Expense User Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShowExpenseApiView(APIView):
    """
    List all expenses and newly created.
    """

    def get(self, request, format=None):
        debts = Expense.objects.all()
        serializer = ExpenseSerializer(debts, many=True)
        return Response(serializer.data)
    # serializer_class = ExpenseSerializer


class CreateExpenseApiView(APIView):
    def post(self, request):
        # import ipdb;
        # ipdb.set_trace()
        user = request.data.get('user')
        user_obj = UserProfile.objects.get(id=user)
        name = user_obj.name

        expense_group = request.data.get('expense_group')
        expense_obj = Group.objects.get(id=expense_group)

        description = request.data.get('description')
        amount = request.data.get('amount')

        repayments = request.data.get('repayments')

        paid_owed = request.data.get('paid_owed')

        expenses_made = Expense.objects.create(
            user=user_obj, expense_group=expense_obj, description=description, amount=amount)

        for repay in repayments:
            repayments_list = Debt.objects.get(id=repay)
            if repayments_list:
                expenses_made.repayments.add(
                    Debt.objects.get(id=repayments_list.id))
                expenses_made.save()

        for paid in paid_owed:
            paid_owed_list = ExpenseUser.objects.get(id=paid)
            if paid_owed_list:
                expenses_made.paid_owed.add(
                    ExpenseUser.objects.get(id=paid_owed_list.id))
                expenses_made.save()

        response = dict()
        response['data'] = name
        response['status'] = status.HTTP_201_CREATED
        response['message'] = "Debts Created Amongst Group"
        return Response(response)


class AddExpensesApiView(APIView):
    def post(self, request):
        serializer = AddExpenseSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # import ipdb;
            # ipdb.set_trace()

            description = request.data.get('description')
            amount = request.data.get('amount')
            paid_by = request.data.get('paid_by')
            to_members = request.data.get('to_members')
            to_group = request.data.get('to_group')

            paid_obj = UserProfile.objects.get(id=paid_by)
            group_obj = Group.objects.get(id=to_group)
            split_choices = request.data.get('split_choices')
            
            print(description)
            print(amount)
            print(to_members)         
            print(paid_obj)
            print(group_obj)            
            print(split_choices, "Split Choice", "Equally")


            new_expense = AddExpense.objects.create(description=description, amount=amount, paid_by=paid_obj, to_group=group_obj)
            print(new_expense)


            if split_choices == AddExpense.BY_EQUALLY:
                user_count = group_obj.members.count()
                print(user_count, "User Count")
                per_member_share = amount / user_count
                print(per_member_share, "Per Member Share")
                new_expense.group_obj = per_member_share
                new_expense.save()

            elif split_choices == AddExpense.BY_UNEQUALLY:
                for member in to_members:
                    print(member)
                    selected_members = UserProfile.objects.get(id=member)
                    if selected_members:
                        new_expense.to_members.add(UserProfile.objects.get(id=selected_members.id))
                        new_expense.split_choices = AddExpense.BY_UNEQUALLY
                        new_expense.save()


            elif split_choices == AddExpense.BY_PERCENTAGE:
                from_member = paid_obj
                print(from_member, "From Member")
                for member in to_members:
                    selected_members = UserProfile.objects.get(id=member)
                    print(selected_members, "Selected Members")
                    quotient = amount / 100
                    percent = quotient * 100
                    print(percent, "Percentage")
                    new_expense.to_members.add(UserProfile.objects.get(id=selected_members.id))
                    new_expense.split_choices = AddExpense.BY_PERCENTAGE
                    new_expense.save()       
                    
            return Response({"status": "New Expenses Added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseReviewViewSet(ModelViewSet):
    queryset = ExpenseReview.objects.all()
    serializer_class = ExpenseReviewSerializer