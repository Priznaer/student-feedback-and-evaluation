from django.db import models
from django.contrib.auth.models import User
import uuid



class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=(("M", "Male"), ("F", "Female")))

    def __str__(self):
        return self.user.get_full_name()


class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3, choices=((1, 1), (2, 2), (3, 3)))
    Lecturers = models.ManyToManyField(Lecturer)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Programme(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_programme'
            )
        ]


class CourseList(models.Model):
    courses = models.ManyToManyField(Course)
    programme = models.ForeignKey(Programme, on_delete=models.PROTECT, related_name="course_lists")
    semester = models.IntegerField(default=100, choices=((1, "First"), (2, "Second")))
    level = models.IntegerField(default=100, choices=((100, 100), (200, 200), (300, 300), (400, 400)))

    def __str__(self):
        return f"{self.programme} - Lvl{self.level} - Sem{self.semester}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['programme', 'level', 'semester'],
                name='unique_course_list'
            )
        ]


class Student(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    index_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=(("M", "Male"), ("F", "Female")))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    semester = models.IntegerField(choices=((1, "First"), (2, "Second")))
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    level = models.IntegerField(default=100, choices=((100, 100), (200, 200), (300, 300), (400, 400)))

    def __str__(self):
        return f"Student: {self.uid}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['index_number'],
                name='unique_student'
            )
        ]


class Classroom(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_classroom'
            )
        ]

        ordering = ["name"]


class Feedback(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    datetime = models.DateTimeField(auto_now=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, editable=False)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    response = models.JSONField()

    def __str__(self):
        return f"Feedback: {self.datetime.date()} <> {self.datetime.strftime('%I:%M%p')} <> ({self.uid})"

    class Meta:
        ordering = ["datetime"]


class Report(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now=True, verbose_name="Created on")
    criteria = models.JSONField()

    def __str__(self):
        return f"Report: {self.creation_datetime.date()} <> {self.creation_datetime.strftime('%I:%M%p')} <> ({self.uid})"

    class Meta:
        ordering = ["creation_datetime"]



