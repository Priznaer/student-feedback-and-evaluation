from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Lecturer, Course, CourseList, Report, Programme, Student, Feedback, Classroom

# super_admin :: DefaultSuperPass
# 2025pass


class CourseListInline(admin.TabularInline):
    model = CourseList
    extra = 0


class ProgrammeAdmin(admin.ModelAdmin):
    inlines = [CourseListInline]


class LecturerAdmin(admin.ModelAdmin):
    # Display all the User fields along with Lecturer fields
    list_display = ['username', 'first_name', 'last_name', 'gender']

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def username(self, obj):
        return obj.user.username

    def email(self, obj):
        return obj.user.email


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ("uid", "creator", "creation_datetime" , "criteria")


class StudentAdminForm(forms.ModelForm):
    # Include fields from the related User model
    username    = forms.CharField(max_length=255)
    email       = forms.EmailField()
    first_name  = forms.CharField(max_length=100)
    last_name   = forms.CharField(max_length=100)
    password    = forms.CharField(max_length=100)

    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # Pre-fill the form fields with the related user data if it's an existing Student
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.user:
            self.instance.user.username     = self.cleaned_data['username']
            self.instance.user.email        = self.cleaned_data['email']
            self.instance.user.first_name   = self.cleaned_data['first_name']
            self.instance.user.last_name    = self.cleaned_data['last_name']
            self.instance.user.save()
        if commit:
            instance.save()
        return instance

class StudentAdmin(admin.ModelAdmin):
    # form = StudentAdminForm
    # fields = ["first_name", "last_name", "gender", "email", "index_number", "programme", "level", "semester"]
    ...



class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ("uid", "datetime", "lecturer", "classroom", "response")


class CustomUserAdmin(UserAdmin):
    ordering = ('-is_staff',)  # Change this to your desired ordering field

    def get_readonly_fields(self, request, obj=None):
        # Define fields that should be readonly
        readonly = ['last_login', 'date_joined']
        if not request.user.is_superuser:
            readonly += ['is_superuser', 'user_permissions']
        return readonly

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Check if the user is not a superuser
        if not request.user.is_superuser:
            student_uids = Student.objects.values_list('user_id', flat=True)  # Get user IDs of all students
            super_admin_id = User.objects.get(is_superuser=True).id
            return qs.exclude(id__in=student_uids).exclude(id=super_admin_id)  # Exclude those user IDs from the queryset
        return qs

# Unregister the default User admin
admin.site.unregister(User)

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)

admin.site.register(Course)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Classroom)
admin.site.register(Report, ReportAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Programme, ProgrammeAdmin)

