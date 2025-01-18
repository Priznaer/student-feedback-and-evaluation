import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_feedback.settings")
django.setup()

from django.contrib.auth.models import User, Group
from core.models import Lecturer, Course, Student, Programme


lecturer_gender_courses = [
    ("Thomas.Boakye",           "M", ("Introduction to Electronics", )), 
    ("Frank.Boateng",           "M", ("Introduction to Computer Systems", )), 
    ("Opoku.Gyabaah",           "M", ("Linear Algebra", "Probability & Statistics", )), 
    ("Abigail.Wiafe",           "F", ("System Analysis & Design", )), 
    ("Veronica.Agblewornu",     "F", ("Computer Architecture", "Data Structures & Algorithms", )), 
    ("Appiah.Kubi",             "M", ("Data Communications & Networking", )), 
    ("Michael.Tabiru",          "M", ("Basic French I", "Basic French II", "Functional French", )), 
    ("Nicholas.Adorsu",         "M", ("Functional French", )), 
    ("Ben.Asante",              "M", ("Applied Chemistry", "General Chemistry", )), 
    ("Gifty.Budu",              "F", ("Communication Skills I", "Communication Skills II", "Technical Report Writing", "English Language I", )), 
    ("Theophilus.Amartey",      "M", ("Basic Mechanics", "Applied Physics", )), 
    ("Eric.Boateng",            "M", ("Environmental Studies", )), 
    ("Emmanuel.Mensah",         "M", ("Engineering mathematics I", "Introductory Electricity & Magnetism", )), 
    ("Moses.Aggor",             "M", ("Principles of Programming", )), 
    ("Philip.Kisembe",          "M", ("Computer Programming For Engineering Application", )), 
    ("Michael.Xenya",           "M", ("Digital Logic", "VLSI & Embedded System Design", )), 
    ("Ibrahim.Gedel",           "M", ("Engineering Technology", )), 
    ("Patricia.Mankatah",       "F", ("Communication Skills I", "Communication Skills II", "Technical Report Writing", )), 
    ("Emmanuel.Kyere-frimpong", "M", ("Physics For Computer Science", )), 
    ("Kwabena.Agyenim-boateng", "M", ("Principles Of Entrepreneurship", )), 
    ("Bernard.Arpoh-baah",      "M", ("General Physics", )), 
    ("Alex.Antwi-adjei",        "M", ("Computer Networking", )), 
    ("Albert.Owusu",            "M", ("System Design & Simulation", )), 
    ("Owusu.Antwi",             "M", ("System Design & Simulation", )), 
    ("Samuel.Addo",             "M", ("Basic Economics", )), 
    ("Emmanuel.Effah",          "M", ("Control Theory", )), 
    ("Samuel.Afoakwa",          "M", ("Electromagnetic Wave Theory", )), 
    ("Daniel.Ngala",            "M", ("Communication Electronics", )), 
    ("Attah.Kumah",             "M", ("Principles Of Accounting & Management", )),
    ("Seth.Frimpong",           "M", ("African Studies", )), 
    ("Eugene.Bazongoly",        "M", ("Integral Calculus", )), 
    ("Grace.Goka",              "F", ("Integral Calculus", )),
    ("Ruhiya.Abubakar",         "F", ("Research Seminars & Presentation", )), 
    ("Emmanuel.Freeman",        "M", ("Programming & Problem-solving", )), 
    ("Isaac.Hanson",            "M", ("Introduction To Microcomputer Systems & Applications", )), 
    ("Ivy.Panyne",              "F", ("Transformers & Electromechanical Energy Conversion", )), 
    ("Eric.Amoateng",           "M", ("Linear Electronics", )), 
    ("Prince.Adeti",            "M", ("DC Machines", )), 
    ("Joseph.Danso",            "M", ("Web Programming & Applications", )), 
    ("Louis.Osei",              "M", ("Applied Electricity", )), 
    ("Denis.Gookyi",            "M", ("Strength Of MAterials", )), 
    ("Ekow.Appiah",             "M", ("Digital Control Systems", )), 
    ("Solomon.Anabiah",         "M", ("High Voltage Engineering", )), 
    ("Josiah.Andoh",            "M", ("Industrial Control", )), 
    ("Stephen.Okrah",           "M", ("Power Electronics", )), 
    ("Francis.Gyimah",          "M", ("Power System Analysis", )), 
    ("Clemence.Dupey",          "M", ("Substation & Transmission Line Design", )), 
    ("Cletus.Mbowura",          "M", ("Logic & Critical Thinking", )), 
    ("Samuel.Danso",            "M", ("Operating Systems", )), 
    ("Samuel.Nortey",           "M", ("Digital Control Systems", )), 
    ("Edward.Boahen",           "M", ("Embedded Systems", )), 
    ("Patrick.Acheampong",      "M", ("Artificial Intelligence", )), 
    ("Anthony.Kwarteng",        "M", ("Discrete Mathematics", )), 
    ("Doreen.Odame",            "F", ("Electrical Heating & Cooling", )), 
    ("Dominic.Loius",           "M", ("Power System Protection", )), 
    ("Martin.Ujakpa",           "M", ("Switch Engineering In Communication", )), 
    ("George.Anni",             "M", ("Moral & Ethics", )), 
    ("William.Acquaye",         "M", ("Analogue Communication", )), 
    ("Stephen.Asunka",          "M", ("Digital Electronics", )), 
    ("Philomena.Ofori",         "M", ("Microwave Technology", )), 
    ("Forgor.Lempogo",          "M", ("Signals & Systems", )), 
    ("Boahemaa.Brenya",         "F", ("Field Theory", )), 
    ("Rexford.Sosu",            "M", ("Linear Electronics", )), 
    ("Alfred.Coleman",          "M", ("Communication Electronics", )), 
    ("Fred.Sarfo",              "M", ("Basic Economics, Accounting & Management", )), 
    ("Thomas.Henaku",           "M", ("Microprocessor Systems & Interfacing", ))
]

students = [
    ("1123456789", "Level-100.Semester-1", 100, 1), ("123456789", "Level-100.Semester-2", 100, 2),
    ("2123456789", "Level-200.Semester-1", 200, 1), ("223456789", "Level-200.Semester-2", 200, 2),
    ("3123456789", "Level-300.Semester-1", 300, 1), ("323456789", "Level-300.Semester-2", 300, 2),
    ("4123456789", "Level-400.Semester-1", 400, 1), ("423456789", "Level-400.Semester-2", 400, 2),
]

admins = [
    ("Derick.Agyepong", "Admin"), ("Phillip.Kove", "Admin"),
    ("Benjamin.Acheampong", "Academic"), ("Rosalinda.Lee", "Academic"),
    ("Orlando.Akorati", "Quality Assurance"), ("William.Antwi", "Quality Assurance"),
]

programme_courselist = {
    "BSc. Computer Science" : (
        (), (),
        (), (),
        (), (),
        (), (),
    ),
    "Bsc. Engineering" : (
        (), (),
        (), (),
        (), (),
        (), (),
    ),
    "BSc. Business Administration" : (
        (), (),
        (), (),
        (), (),
        (), (),
    ),
}

groups = ("Admin", "Academic", "Quality Assurance")

password    = "2025pass"



# Create Groups
# ...

# # Create admins
# for username, group in admins:
#     group = Group.objects.get(name=group)
#     first, last     = username.split(".")
#     user, created   = User.objects.get_or_create(username=username, is_staff=True)
#     user.first_name = first
#     user.last_name  = last
#     user.set_password(password)
#     user.groups.add(group)
#     user.save()
    # print(f"Username :: {username}\nFirst :: {user.first_name}\nLast :: {user.last_name}\nGroups :: {user.groups.all()}\n")

# # Create students
# for idx, (index_number, name, level, semester) in enumerate(students):
#     first, last = name.split(".")
#     genders = ("M", "F")
#     gender = genders[idx%2]
#     user, user_created = User.objects.get_or_create(username=index_number, first_name=first, last_name=last)
#     if user_created:
#         user.set_password(password)
#         user.save()
#     programme = Programme.objects.get(name="BSc. Computer Science")
#     student, student_created = Student.objects.get_or_create(index_number=index_number, gender=gender, user=user, semester=semester, programme=programme, level=level)
#     if student_created:
#         student.save()
#     print(f"{idx} >> {index_number} >> {name} >> {level} >> {semester} >> {gender}")


# # Create lecturers
# for username, gender, courses in lecturer_gender_courses:
#     first, last = username.split(".")
#     print(f"first :: {first} last :: {last}")
#     user, created   = User.objects.get_or_create(username=username, first_name=first, last_name=last)
#     if created:
#         user.set_password(password)
#         user.save()
#     lecturer, created = Lecturer.objects.get_or_create(user=user, gender=gender)
#     if not lecturer:
#         lecturer = Lecturer(
#             user=user,
#             gender=gender
#         )
#         lecturer.save()
#     # Create courses
#     for course_name in courses:
#         course, created = Course.objects.get_or_create(name=course_name)
#         course.Lecturers.add(lecturer)
#         course.save()

# else:
#     print("Done")

print("<<< End Reached >>>")