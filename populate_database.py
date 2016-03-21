import os
import django
from random import randint

departments = {
    "Computer Science": ["Comp Room1", "Comp Room2"],
    "Maths": ["Math Room 1", "Math Room 2"],
    "Biology": ["Biology Room 1", "Biology Room 2"],
    "Architecture": ["Architecture Room 1", "Architecture Room 2"],
    "Mechanical Engineering": ["Mech Eng Room 1", "Mech Eng Room 2"],
    "Electronic Engineering": ["Elec Eng Room 1", "Elec Eng Room 2"],
    "Physics": ["Physics Room 1", "Physics Room 2"],
    "Chemistry": ["Chemistry Room 1", "Chemistry Room 2"]
}


def populate():

    # Create a new user/student instance: scripty
    user = User.objects.create_user('scripty', 'jack@evans.gb.net', 'scripty')
    student = Student.objects.get_or_create(user=user)[0]
    user.save(), student.save()

    for key, values in departments.items():
        print("Adding: " + key)
        department = add_department(key)
        for space in values:
            studyspace = add_studyspace(department, space)
            # Creates a random amount (max 500) of random ratings for each
            # studyspace ◕‿◕
            ratings = [
                Rating(studyspace=studyspace, rating=randint(1, 5),
                       student=student) for i in range(1, randint(1, 500))
            ]
            Rating.objects.bulk_create(ratings)
            studyspace.save()

    # Delete poor scripty :(
    user.delete(), student.delete()


def add_department(name):
    d = Department.objects.get_or_create(department_name=name)[0]
    return d


def add_studyspace(department, name):
    s = StudySpace.objects.get_or_create(
        department=department,
        space_name=name
    )[0]
    return s

if __name__ == '__main__':
    print("Starting spacefinder population script...\n")
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        'IntegratedProject.settings'
    )
    django.setup()

    from spacefinder.models import Department, StudySpace, Rating, Student
    from django.contrib.auth.models import User

    # Wipe our existing database records
    # ┌∩┐(◕_◕)┌∩┐
    Department.objects.all().delete()
    populate()
