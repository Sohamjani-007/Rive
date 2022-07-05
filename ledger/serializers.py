from django.contrib.auth import get_user_model
from rest_framework import serializers
from ledger.models import *

User = get_user_model()

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # To support inserts with the value
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password')


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ('id', 'from_user', 'to_user', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'group_name', 'debts', 'members')


class ExpenseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseUser
        fields = ('id', 'user', 'paid_share', 'owed_share', 'net_balance')


class ExpenseSerializer(serializers.ModelSerializer):
    # repayments = serializers.PrimaryKeyRelatedField(queryset=Expense.objects.all(), pk_field=serializers.IntegerField)

    class Meta:
        model = Expense
        fields = ('user', 'name', 'expense_group', 'description',
                  'amount', 'repayments', 'paid_owed', 'transaction_id')


class AddExpenseSerializer(serializers.ModelSerializer):
    # split_choices = ChoiceField(choices=AddExpense.SPLIT_CHOICES)
    class Meta:
        model = AddExpense
        fields = ('description', 'amount', 'paid_by', 'to_members', 'to_group', 'split_choices')

class ExpenseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseReview
        fields = ['expense', 'name', 'description', 'date']
