from django import forms
from .models import Programme, Classroom, Feedback, Lecturer, Course
from django.utils.safestring import mark_safe

from django.utils import timezone
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator



class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    remember = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "id": "username",
        })
        self.fields["password"].widget.attrs.update({
            "id": "password",
        })
        self.fields["remember"].widget.attrs.update({
            "id": "remember",
        })


class CustomRadioSelect(forms.RadioSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Render the radio buttons and add custom attributes to each input and label
        final_attrs = self.build_attrs(attrs)
        options_html = []
        
        for option_value, option_label in self.choices:
            # Generate unique ID for each option, for example 'radio_id_1'
            custom_id = option_value
            custom_value = option_value  # You can change this if necessary
            custom_name = name  # The radio buttons will share the same name attribute
            
            radio_html = f'<input type="radio" name="{custom_name}" value="{custom_value}" id="{custom_id}"'
            radio_html += f' hidden required/>'
            
            label_html = f'<label for="{custom_id}">{option_label}</label>'
            
            # Combine radio input and label
            options_html.append(f'{radio_html} {label_html}')
        
        return mark_safe('\n'.join(options_html))


class RegistrationForm(forms.Form):
    choices = [("student", "Student"), ("admin", "Admin"), ("lecturer", "Lecturer")]
    account_type = forms.ChoiceField(widget=CustomRadioSelect, choices=choices)
    username = forms.CharField(max_length=50, initial="N/A")
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    index_number = forms.CharField()
    gender_options = (("", "Select Gender"), ("F", "Female"), ("M", "Male"))
    gender = forms.ChoiceField(choices=gender_options, widget=forms.Select())
    programme_options = [("", "Select Programme")] + [(programme.pk, str(programme)) for programme in Programme.objects.all()]
    programme = forms.ChoiceField(choices=programme_options, widget=forms.Select())
    level_options = (("", "Select Level"), ("100", "100"), ("200", "200"), ("300", "300"), ("400", "400"))
    level = forms.ChoiceField(choices=level_options, widget=forms.Select())
    semester_options = (("", "Select Semester"), ("1", "First"), ("2", "Second"))
    semester = forms.ChoiceField(choices=semester_options, widget=forms.Select())
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Password', min_length=8)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "id": "username",
            "placeholder": "Username",
            "class": "non-student",
        })
        self.fields["first_name"].widget.attrs.update({
            "id": "first_name",
            "placeholder": "First Name",
            "required": ""
        })
        self.fields["last_name"].widget.attrs.update({
            "id": "last_name",
            "placeholder": "Last Name",
            "required": ""
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "Email",
        })
        self.fields["index_number"].widget.attrs.update({
            "id": "index_number",
            "class": "student",
            "name": "index_number",
            "placeholder": "Index Number",
        })
        self.fields["gender"].widget.attrs.update({
            "name": "gender",
            "required": ""
        })
        self.fields["programme"].widget.attrs.update({
            "name": "programme",
            "class": "student",
        })
        self.fields["level"].widget.attrs.update({
            "name": "level",
            "class": "student",
        })
        self.fields["semester"].widget.attrs.update({
            "name": "semester",
            "class": "student",
        })
        self.fields["password1"].widget.attrs.update({
            "name": "password1",
            "placeholder": "Enter Password",
            "required": ""
        })
        self.fields["password2"].widget.attrs.update({
            "name": "password2",
            "placeholder": "Confirm Password",
            "required": ""
        })


class FeedbackForm(forms.Form):
    course_options = (("", "Select Course"),)
    course = forms.ChoiceField(choices=course_options, widget=forms.Select())
    lecturer_options = (("", "Select Lecturer"),)
    lecturer = forms.ChoiceField(choices=lecturer_options, widget=forms.Select(), help_text="Select Course To See Corresponding Lecturers")
    classroom_options = [("", "Select Classroom")] + [(classroom.pk, str(classroom)) for classroom in Classroom.objects.all()]
    classroom = forms.ChoiceField(choices=classroom_options, widget=forms.Select())
    q1_options = [("1", "Before time"), ("2", "On time"), ("3", "Slightly late"), ("4", "Very late"), ("5", "Absent")]
    question1 = forms.ChoiceField(widget=forms.RadioSelect, choices = q1_options)
    q2_options = [("1", "Excellent"), ("2", "Good"), ("3", "Average"), ("4", "Poor"), ("5", "Terrible")]
    question2 = forms.ChoiceField(widget=forms.RadioSelect, choices = q2_options)
    q3_options = [("1", "Excellent"), ("2", "Good"), ("3", "Average"), ("4", "Poor"), ("5", "Terrible")]
    question3 = forms.ChoiceField(widget=forms.RadioSelect, choices = q3_options)
    q4_options = [("1", "Excellent"), ("2", "Good"), ("3", "Average"), ("4", "Poor"), ("5", "Terrible")]
    question4 = forms.ChoiceField(widget=forms.RadioSelect, choices = q4_options)
    q5_options = [("1", "Excellent"), ("2", "Good"), ("3", "Average"), ("4", "Poor"), ("5", "Terrible")]
    question5 = forms.ChoiceField(widget=forms.RadioSelect, choices = q5_options)
    q6_options = [("1", "Excellent"), ("2", "Good"), ("3", "Average"), ("4", "Fast"), ("5", "Too Fast")]
    question6 = forms.ChoiceField(widget=forms.RadioSelect, choices = q6_options)
    q7_options = [("1", "Yes"), ("2", "No")]
    question7 = forms.ChoiceField(widget=forms.RadioSelect, choices = q7_options)
    q8_options = [("1", "Excellent"), ("2", "Clear enough"), ("3", "Somewhat clear"), ("4", "Unclear"), ("5", "None Given")]
    question8 = forms.ChoiceField(widget=forms.RadioSelect, choices = q8_options)
    q9_options = [("1", "Yes"), ("2", "Barely"), ("3", "No")]
    question9 = forms.ChoiceField(widget=forms.RadioSelect, choices = q9_options)
    q10_options = [("1", "Excellent"), ("2", "Conducive enough"), ("3", "Somewhat Conducive"), ("4", "Unconducive"), ("5", "Online class")]
    question10 = forms.ChoiceField(widget=forms.RadioSelect, choices = q10_options)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].widget.attrs.update({
            "id": "course",
            "name": "course",
            "required": "",
        })
        self.fields["lecturer"].widget.attrs.update({
            "id": "lecturer",
            "name": "lecturer",
            "required": "",
        })
        self.fields["classroom"].widget.attrs.update({
            "id": "classroom",
            "name": "classroom",
            "required": "",
        })
        self.fields["question1"].widget.attrs.update({
            "id": "question1",
            "required": "",
        })
        self.fields["question2"].widget.attrs.update({
            "id": "question2",
            "required": "",
        })
        self.fields["question3"].widget.attrs.update({
            "id": "question3",
            "required": "",
        })
        self.fields["question4"].widget.attrs.update({
            "id": "question4",
            "required": "",
        })
        self.fields["question5"].widget.attrs.update({
            "id": "question5",
            "required": "",
        })
        self.fields["question6"].widget.attrs.update({
            "id": "question6",
            "required": "",
        })
        self.fields["question7"].widget.attrs.update({
            "id": "question7",
            "required": "",
        })
        self.fields["question8"].widget.attrs.update({
            "id": "question8",
            "required": "",
        })
        self.fields["question9"].widget.attrs.update({
            "id": "question9",
            "required": "",
        })
        self.fields["question10"].widget.attrs.update({
            "id": "question10",
            "required": "",
        })


class ReportGenerateForm(forms.Form):
    # Fetch the first Feedback to set the min and default value for start_date
    first_feedback = Feedback.objects.first()
    start_date_default = first_feedback.datetime.date() if first_feedback else date.today()
    start_year_default = start_date_default.year

    # Date fields
    start_date = forms.DateField(
        initial=start_date_default,
        widget=forms.SelectDateWidget(years=range(start_year_default, 2100)),
        label='Start Date',
        input_formats=['%Y-%m-%d'],
        validators=[MinValueValidator(start_date_default)]  # Setting min_value
    )

    end_date = forms.DateField(
        initial=date.today(),
        widget=forms.SelectDateWidget(years=range(start_year_default, 2100)),
        label='End Date',
        input_formats=['%Y-%m-%d'],
        validators=[MaxValueValidator(date.today())]  # Setting max_value
    )

    # Select fields
    programme = forms.ModelChoiceField(
        queryset=Programme.objects.all(),
        widget=forms.Select(),
        label='Programme'
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),  # Initially empty
        widget=forms.Select(),
        label='Course'
    )

    classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all(),
        widget=forms.Select(),
        label='Classroom'
    )
    
    lecturer = forms.ModelChoiceField(
        queryset=Lecturer.objects.none(),  # Initially empty
        widget=forms.Select(),
        label='Lecturer'
    )

