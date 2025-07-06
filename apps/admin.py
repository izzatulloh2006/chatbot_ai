from django.contrib import admin
from .models import User, Question

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name', 'created_at')
    search_fields = ('user_id', 'username', 'first_name')
    list_filter = ('created_at', )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("user_id", "username", "question", "answer", "language", "created_at")
    search_fields = ("username", "question")
    list_filter = ("language", "created_at")
