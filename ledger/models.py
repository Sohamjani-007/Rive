from tabnanny import verbose
import time
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


# Create your models here.


class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """

    def create_user(self, email, password=None) -> "UserProfile":
        if not email:
            raise ValueError("Invalid Email")
        # normalize email, convert second half to lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self.db)
        return user


class UserProfile(AbstractBaseUser):
    """ Database model for users in system """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self) -> str:
        """
        Retrieve full name of user
        :return: str
        """
        return self.name  # The user is identified by their name

    def get_short_name(self) -> str:
        """
        Retrieve short name of user
        :return: str
        """
        return self.name  # The user is identified by their name

    def __str__(self) -> str:
        """
        Return String representation of User
        :return: str
        """
        return f"Email: {self.email}, Name:{self.name}"  # The user is identified by their name


class Debt(models.Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='from_user', null=True)
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='to_user', null=True)
    amount = models.IntegerField()
    # def __str__(self) -> str:
    #     return f'{self.to_user.name} owes {self.amount} to {self.from_user.name}'


class Group(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(max_length=255, unique=True) 
    debts = models.ManyToManyField(Debt, blank=True, related_name='debts')
    members = models.ManyToManyField(UserProfile)
    class Meta:
        verbose_name_plural = 'group'


class ExpenseUser(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    paid_share = models.IntegerField(default=0)
    owed_share = models.IntegerField(default=0)
    net_balance = models.IntegerField(default=0)


class Expense(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    expense_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, db_constraint=False)
    description = models.CharField(max_length=255)
    payment = models.BooleanField(default=False)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    repayments = models.ManyToManyField(Debt)
    paid_owed = models.ManyToManyField(ExpenseUser)
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class AddExpense(models.Model):
    BY_EQUALLY = "E"          
    BY_UNEQUALLY = "U"
    BY_PERCENTAGE = "P"

    SPLIT_CHOICES = [
        (BY_EQUALLY, 'Equally'),
        (BY_UNEQUALLY, 'Unequally'),
        (BY_PERCENTAGE, 'Percentage'),
    ]
    description = models.CharField(max_length=255)
    amount = models.IntegerField()
    paid_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='paid_by')
    to_members = models.ManyToManyField(UserProfile)
    to_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    split_choices = models.CharField(max_length=30, choices=SPLIT_CHOICES, default=BY_EQUALLY)


class ExpenseReview(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    