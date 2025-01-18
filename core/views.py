from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm, FeedbackForm, ReportGenerateForm
from .models import Feedback, Lecturer, Programme, Report, Student, CourseList, Course, Classroom
import datetime as datetime_main
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
from django.conf import settings
from pprint import pprint



def login_page(request):
    if request.user.is_authenticated:
        notification = "You are already logged in."
        return redirect("home/", notification=notification)
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember = form.cleaned_data["remember"]
            authenticated_user = authenticate(username=username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("home/")
            else:
                form.add_error(None, "Invalid Username or Password")
    else:
        form = LoginForm()
    return render(request, "core/login.html", {'form':form})

@login_required(login_url="/")
def homepage(request, notification=None):
    user = request.user
    if Student.objects.filter(user=user).exists():
        return redirect("/create-feedback/", notification=notification)
    elif Lecturer.objects.filter(user=user).exists():
        lecturer = Lecturer.objects.get(user=user)
        all_lecturer_feedbacks = Feedback.objects.filter(lecturer=lecturer)
        context = {
            "notification"              : notification,
            "all_lecturer_feedbacks"    : all_lecturer_feedbacks,
            "lecturer_feedbacks_today"  : list(),
        }
        for lecturer_fb in all_lecturer_feedbacks:
            if lecturer_fb.datetime.date() == datetime.today().date():
                context["lecturer_feedbacks_today"].append(lecturer_fb)
        return render(request, "core/lecturer_home.html/", context)
    else:
        if request.user.username != "super_admin":
            user_group = request.user.groups.all().first().name
            admin.site.site_header = user_group.title() + " Database Interface"
            admin.site.site_title = "DB Interface"
            # admin.site.index_title = "".join([name[0] for name in user_group.title().split()]) + " Site Data"
            admin.site.index_title = user_group + " Site Data"
        all_feedbacks   = Feedback.objects.all()
        feedbacks_today = Feedback.objects.filter(datetime__date=datetime.today().date())
        all_reports     = Report.objects.all()
        reports_today   = Report.objects.filter(creation_datetime__date=datetime.today().date())
        context = {
            "notification"      : notification,
            "all_feedbacks"     : all_feedbacks,
            "feedbacks_today"   : feedbacks_today,
            "all_reports"       : all_reports,
            "reports_today"     : reports_today,
            "isAdmin"           : True,
        }
        return render(request, "core/admin_home.html/", context)

@login_required(login_url="/")
def help_page(request):
    return render(request, "core/help_page.html")

@login_required(login_url="/")
def create_feedback(request, notification=None):
    student = Student.objects.filter(user=request.user).exists()
    if not student:
        return render(request, "core/access_denied_page.html")
    else: 
        student      = Student.objects.get(user=request.user)
        course_list  = student.programme.course_lists.all().filter(semester=student.semester, level=student.level)
        course_objs  = [course for course in course_list.first().courses.all()]
        courses_dict = {course.pk: str(course) for course in course_list.first().courses.all()}
        
        lecturers_dict  = dict()
        for course in course_objs:
            lecturers   = {lecturer.pk: str(lecturer) for lecturer in course.Lecturers.all()}
            lecturers_dict[course.pk] = lecturers

    if request.method   == "POST":
        form            = FeedbackForm(request.POST)
        request_values  = list(request.POST.values())
        course_pk       = request.POST.get("course")
        course          = Course.objects.get(pk=course_pk)
        lecturer_pk     = request.POST.get("lecturer")
        lecturer        = Lecturer.objects.get(pk=lecturer_pk)
        form.is_valid()
        classroom_pk    = form.cleaned_data.pop("classroom")
        classroom       = Classroom.objects.get(pk=classroom_pk)
        response_list   = [int(response) for response in form.cleaned_data.values()] #list(form.cleaned_data.values())
        # validate there hasn't been a feedback for the course today
        feedbacks_today = Feedback.objects.filter(student=student, course=course)
        for course_feedback in feedbacks_today:
            if course_feedback.datetime.date() == datetime.today().date():
                error_message = "You have already evaluated this lecture today"
                return render(request, "core/feedback_error_page.html", {"error_message":error_message})
        # save feedback
        new_feedback = Feedback(
            student=student,
            lecturer=lecturer,
            course = course,
            classroom=classroom,
            response=response_list
        )
        new_feedback.save()
        return render(request, "core/done.html")
    else:
        form    = FeedbackForm()
        context = {
            "form"          : form, 
            "isStudent"     : True,
            "course_names"  : courses_dict,
            "notification"  : notification,
            "lecturers_dict": lecturers_dict, 
        }
    return render(request, "core/feedback_form_page.html", context)

@login_required(login_url="/")
def done_page(request):
    return render(request, "core/done.html")

@login_required(login_url="/")
def view_feedback(request, feedback_pk):
    user = request.user
    if Student.objects.filter(user=user).exists():
        return render(request, "core/access_denied_page.html")
    feedback_exists = Feedback.objects.filter(pk=feedback_pk).exists()
    if not feedback_exists:
        return render(request, "core/page_not_found.html", {"feedback":feedback})
    else:
        data = {
            "uid"       : None,
            "date"      : None,
            "time"      : None,
            "lecturer"  : None,
            "course"    : None,
            "classroom" : None,
            "question1" : None,
            "question2" : None,
            "question3" : None,
            "question4" : None,
            "question5" : None,
            "question6" : None,
            "question7" : None,
            "question8" : None,
            "question9" : None,
            "question10": None,
        }
        retrieved_feedback  = Feedback.objects.get(pk=feedback_pk)
        data["uid"]         = retrieved_feedback.uid
        data["date"]        = retrieved_feedback.datetime.strftime("%d %b, %Y")
        data["time"]        = retrieved_feedback.datetime.strftime("%H:%M:%S")
        data["lecturer"]    = retrieved_feedback.lecturer
        data["course"]      = retrieved_feedback.course
        data["classroom"]   = retrieved_feedback.classroom
        for number, response in enumerate(retrieved_feedback.response):
            question_number = "question" + str(number+1)
            data[question_number] = response

        form = FeedbackForm(data=data)
        context = {
            "form"    : form, 
            "data"    : data,
            "isAdmin" : True,
        }
        return render(request, "core/feedback_detail_page.html", context)

@login_required(login_url="/")
def register(request):
    # Check if user has permission for this page
    ...
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            internal_errors = False
            account_type = form.cleaned_data.get("account_type")
            username     = form.cleaned_data.get("username")
            first_name   = form.cleaned_data.get("first_name")
            last_name    = form.cleaned_data.get("last_name")
            email        = form.cleaned_data.get("email")
            index_number = form.cleaned_data.get("index_number")
            gender       = form.cleaned_data.get("gender")
            programme    = form.cleaned_data.get("programme")
            level        = form.cleaned_data.get("level")
            semester     = form.cleaned_data.get("semester")
            password1    = form.cleaned_data.get("password1")
            password2    = form.cleaned_data.get("password2")
            match account_type:
                case "student":
                    if not index_number.isdigit():
                        form.add_error("index_number", "Index number must be only digits")
                        internal_errors = True
                    elif Student.objects.filter(index_number=index_number):
                        form.add_error("index_number", f'Index number {index_number} is already in use.')
                        internal_errors = True
                    else:
                        username = index_number
                case "lecturer" | "admin":
                    if username == "N/A":
                        form.add_error("username", 'Enter a valid username.')
                        internal_errors = True
                    elif User.objects.filter(username=username):
                        form.add_error("username", f'Username {username} is already in use.')
                        internal_errors = True
            if password1 != password2:
                form.add_error("password2", f'Passwords do not match.')
                internal_errors = True
            if internal_errors:
                return render(request, "core/register.html", {"form":form})
            # Create User object
            new_user = User.objects.create(
                username    = username,
                email       = email,
                first_name  = first_name,
                last_name   = last_name,
                password    = password2
            )
            new_user.save()
            match account_type:
                case "student":
                    programme = Programme.objects.get(pk=programme)
                    new_student = Student(
                        user         = new_user,
                        index_number = index_number,
                        gender       = gender,
                        programme    = programme,
                        semester     = semester,
                        level        = level
                    )
                    new_student.save()
                case "lecturer":
                    new_lecturer = Lecturer(
                        user     = new_user,
                        gender   = gender
                    )
                    new_lecturer.save()
            ...
            return HttpResponseRedirect("")
        else:
            for field in form:
                ...
    else:
        form = RegistrationForm()
    return render(request, "core/register.html", {"form":form})

def filter_feedbacks_by_criteria(criteria_dict):
    start_date  = criteria_dict["start_date"]
    end_date    = criteria_dict["end_date"]
    lecturer    = criteria_dict["lecturer"]
    programme   = criteria_dict["programme"]
    course      = criteria_dict["course"]
    classroom   = criteria_dict["classroom"]
    # start filtering
    filtered_feedbacks = Feedback.objects.all()
    if start_date and start_date != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(datetime__date__gte=start_date)
    if end_date and end_date != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(datetime__date__lte=end_date)
    if lecturer and lecturer != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(lecturer=lecturer)
    if classroom and classroom != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(classroom=classroom)
    if programme and programme != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(student__programme=programme)
    if course and course != 'all':
        filtered_feedbacks = filtered_feedbacks.filter(course=course)
    return filtered_feedbacks

def prep_viz_data(filtered_feedbacks):
    data = {
        "Questions" : ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"],
        "Opt-A"     : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Opt-B"     : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Opt-C"     : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Opt-D"     : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Opt-E"     : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    for response_set in [feedback.response for feedback in filtered_feedbacks]:
        for question_number, response in enumerate(response_set):
            match int(response):
                case 1: 
                    data["Opt-A"][question_number] +=1
                case 2:
                    data["Opt-B"][question_number] +=1
                case 3:
                    data["Opt-C"][question_number] +=1
                case 4:
                    data["Opt-D"][question_number] +=1
                case 5:
                    data["Opt-E"][question_number] +=1
    return data

def check_report_exists(criteria_dict):
    # Verify similar report does not exist
    response_dict = {
        "filename"      : None,
        "criteria_dict" : criteria_dict
    }
    all_reports = Report.objects.all()
    for report in all_reports:
        for criteria in criteria_dict:
            if (criteria_dict[criteria] != report.criteria[criteria]):
                break
        else:
            response_dict["filename"] = f"{str(report.uid)}.html"
    return response_dict

def get_viz_html_src(data_frame, creator, criteria_dict, title):
    # Create an interactive bar chart using Plotly
    fig = px.bar(data_frame, title=title)

    viz_filename, viz_criteria = check_report_exists(criteria_dict).values()

    if not viz_filename:
        # Save the report
        new_report = Report(creator=creator, criteria=viz_criteria)
        new_report.save()
        viz_filename = str(new_report.uid) + ".html"

    viz_filepath = os.path.join(settings.MEDIA_ROOT, viz_filename)
    # Save the chart as an HTML file
    print(f"<<< {viz_filename} >>>")
    print(f"<<< {viz_filepath} >>>")
    fig.write_html(viz_filepath)
    # Pass the URL of the saved chart to the template
    viz_src = os.path.join(settings.MEDIA_URL, viz_filename)
    return viz_src

@login_required(login_url="/")
def generate_report(request):
    context = {
        "error_message" : None,
        "viz_src"       : None,
        "processed"     : False,
    }
    user = request.user
    if Student.objects.filter(user=user).exists() or Lecturer.objects.filter(user=user).exists():
        return render(request, "core/access_denied_page.html")
    # Create report form
    if request.method == "POST":
        form = ReportGenerateForm(request.POST)
        # Verify end_date is after start_date
        if (datetime_main.date(int(request.POST.get('start_date_year')), int(request.POST.get('start_date_month')), int(request.POST.get('start_date_day'))) > 
            datetime_main.date(int(request.POST.get('end_date_year')), int(request.POST.get('end_date_month')), int(request.POST.get('end_date_day')))):
            print(">>>> Date Error <<<<<<<<")
            pprint(request.POST)
            context["error_message"] = "DateError :: 'Start Date' must be before 'End Date'"
        if not context["error_message"]:
            form.is_valid()
            # compile criteria dictionary
            criteria_dict = dict()
            criteria_dict["start_date"]  = f"{request.POST.get('start_date_year')}-{request.POST.get('start_date_month')}-{request.POST.get('start_date_day')}"
            criteria_dict["end_date"]    = f"{request.POST.get('end_date_year')}-{request.POST.get('end_date_month')}-{request.POST.get('end_date_day')}"
            criteria_dict["lecturer"]    = request.POST.get("lecturer")
            criteria_dict["programme"]   = request.POST.get("programme")
            criteria_dict["course"]      = request.POST.get("course")
            criteria_dict["classroom"]   = request.POST.get("classroom")

            # filter feedback objects based on report criteria
            filtered_feedbacks = filter_feedbacks_by_criteria(criteria_dict)
            if len(filtered_feedbacks):
                # Prepare visualization data
                data = prep_viz_data(filtered_feedbacks) 

                # Create dataFrame
                df = pd.DataFrame(data)
                df = df.set_index("Questions")

                # Get and pass visualization path to template
                context["viz_src"] = get_viz_html_src(df, request.user, criteria_dict, title="Report Visualization")
            else:
                context["viz_src"] = None
            context["processed"] = True

            # Reset form to default values
            form = ReportGenerateForm()
    else:
        form = ReportGenerateForm()
    context["form"] = form
    return render(request, "core/report_creation_form_page.html", context)

@login_required(login_url="/")
def get_courses(request):
    # Retrieve the selected programme ID from the request
    programme_id = request.GET.get('programme_id')
    if programme_id:
        # Get all courses related to this programme
        try:
            programme = Programme.objects.get(id=programme_id)
            course_lists = CourseList.objects.filter(programme=programme)
            courses = [{"id":"", "name":"-----------------"}, {"id":"all", "name":"All"}]

            for course_list in course_lists:
                for course in course_list.courses.all():
                    courses.append({
                        'id': course.id,
                        'name': course.name
                    })

            # Create the HTML options for the courses
            courses_html = ''.join([f'<option value="{course["id"]}">{course["name"]}</option>' for course in courses])
            return JsonResponse({'courses_html': courses_html})

        except Programme.DoesNotExist:
            return JsonResponse({'courses_html': [{"id":"", "name":"-----------------"}, {"id":"all", "name":"All"}]})    
    return JsonResponse({'courses_html': [{"id":"", "name":"-----------------"}, {"id":"all", "name":"All"}]})

@login_required(login_url="/")
def get_lecturers(request):
    # Retrieve the selected course ID from the request
    course_id = request.GET.get('course_id')
    if course_id == "all":
        lecturers = Lecturer.objects.all()
        lecturers_html = ''.join([f'<option value="{lecturer.id}">{lecturer.user.get_full_name()}</option>' for lecturer in lecturers])
        lecturers_html = '<option value="all">All</option>' + lecturers_html
        return JsonResponse({'lecturers_html': lecturers_html})
    elif course_id == "":
        return JsonResponse({'lecturers_html': '<option value="">---------</option>'})
    if course_id:
        # Get all lecturers related to this course
        try:
            course = Course.objects.get(id=course_id)
            lecturers = course.Lecturers.all()

            # Create the HTML options for the lecturers
            lecturers_html = ''.join([f'<option value="{lecturer.id}">{lecturer.user.get_full_name()}</option>' for lecturer in lecturers])
            lecturers_html = '<option value="all">All</option>' + lecturers_html
            return JsonResponse({'lecturers_html': lecturers_html})

        except Course.DoesNotExist:
            return JsonResponse({'lecturers_html': '<option value="all">All</option>'})
    return JsonResponse({'lecturers_html': '<option value="all">All</option>'})

@login_required(login_url="/")
def view_report(request, report_pk):
    report = Report.objects.filter(pk=report_pk).first()
    viz_filename = str(report.uid) + ".html"
    viz_src = viz_src = os.path.join(settings.MEDIA_URL, viz_filename)
    if not report:
        return render(request, "core/page_not_found.html")
    context = {
        "viz_src"   : viz_src, 
        "report"    : report,
        "criteria"  : {
            "start_date"    : report.criteria["start_date"],
            "end_date"      : report.criteria["end_date"],
            "lecturer"     : None,
            "programme"     : None,
            "course"        : None,
            "classroom"     : None,
        }
    }
    for criteria_key in report.criteria:
        criteria_value = report.criteria[criteria_key]
        if (criteria_value.isdigit()):
            criteria_pk = int(criteria_value)
            match criteria_key:
                case "lecturer":
                    criteria_value = Lecturer.objects.get(pk=criteria_pk)
                case "programme":
                    criteria_value = Programme.objects.get(pk=criteria_pk)
                case "course":
                    criteria_value = Course.objects.get(pk=criteria_pk)
                case "classroom":
                    criteria_value = Classroom.objects.get(pk=criteria_pk)
        else:
            criteria_value = criteria_value.title()
        context["criteria"][criteria_key] = criteria_value
    return render(request, "core/report_detail_page.html", context)

@login_required(login_url="/")
def logout_user(request):
    logout(request)
    return redirect("/")

def custom_page_not_found(request, exception):
    return render(request, 'core/404.html', status=404)