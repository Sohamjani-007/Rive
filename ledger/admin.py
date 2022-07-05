from django.contrib import admin
from ledger import models
# Register your models here.

admin.site.register(models.ExpenseUser)
admin.site.register(models.UserProfile)
admin.site.register(models.Debt)
admin.site.register(models.Group)
admin.site.register(models.Expense)
admin.site.register(models.AddExpense)