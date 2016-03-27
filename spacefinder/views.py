from .forms import UserForm, StudentForm, LoginForm
from .models import StudySpace, Rating, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.messages import get_messages
import datetime


def index(request):
    """Shows list of studyspaces, along with corresponding 'busyness' score"""
    # Sort by average 'busyness' score
    study_space_list = StudySpace.objects.order_by('-avg_rating')

    # Load information to pass to the view
    context = {
        'study_space_list': study_space_list,
        'user_form': UserForm(),
        'student_form': StudentForm(),
        'login_form': LoginForm(auto_id=False),
        'notifications': [str(message) for message in get_messages(request)]
    }

    # If the user is logged in then we need to fetch their student details
    if request.user.is_authenticated():
        context['user'] = request.user

    return render(request, 'spacefinder/index.html', context)


def profile(request, slug):
    """Individual user profile page"""
    student = request.user.student
    ratings = Rating.objects.filter(student=student)
    return render(request, 'spacefinder/profile.html',
                  {'student': student, 'ratings': ratings})


def detail(request, slug):
    """ Page to display detailed information about each studyspace."""
    # Load study space information to pass to the view
    studyspace = get_object_or_404(StudySpace, slug=slug)

    # Load all the ratings associated with this studyspace
    rating_objects = Rating.objects.filter(studyspace=studyspace)
    rating_objects = rating_objects.order_by('timestamp')

    # Get the last 50 votes
    latest_ratings = [[rating.timestamp.isoformat(), rating.rating] for rating
                      in rating_objects[:50][::-1]]

    # Get the average from the last 24 Hours
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    days_ratings = [[rating.timestamp.isoformat(), rating.rating] for rating in
                    rating_objects.filter(timestamp__range=[yesterday, today])]

    print(days_ratings)

    return render(request, 'spacefinder/detail.html', {
        'studyspace': studyspace, 'ratings': latest_ratings,
    })


def vote(request, studyspace_id):
    """ Creates a new rating record when the vote button is pressed."""
    # If I accidently try to vote as admin
    if request.user.is_superuser:
        messages.error(request, "You're logged in as Admin")
    # If users are authenticated, proceed as normal
    elif request.user.is_authenticated():
        # Get a copy of the corresponding studyspace object for that page
        studyspace = get_object_or_404(StudySpace, pk=studyspace_id)
        # Get the value of the users score
        score = request.POST['choice']
        # Update 'busyness' score
        Rating(
            studyspace=studyspace,
            student=request.user.student,
            rating=score).save()
        studyspace.save(update_fields=['avg_rating'])
        return HttpResponseRedirect(reverse('spacefinder:index'))
    # If user is not authenticated at all
    else:
        messages.error(request, "Must be logged in to vote!")
    # Reload current page + error message if unauthorised user attempts to vote
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
    """Allow new users to Register an account"""
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        student_form = StudentForm(data=request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Delays saving the model in order  to avoid integrity problems
            student = student_form.save(commit=False)
            student.user = user
            if 'avatar' in request.FILES:
                student.avatar = request.FILES['avatar']
            student.save()
        else:
            print(user_form.errors, student_form.errors)
    return HttpResponseRedirect(reverse('spacefinder:index'))


def user_login(request):
    """Allows users to login"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "Login Successful")
            else:
                messages.error(request, "Incorrect password!")
        except User.DoesNotExist:
            messages.error(request, "Unknown Username")
    return HttpResponseRedirect(reverse('spacefinder:index'))


@login_required
def user_logout(request):
    """Allows users to logout"""
    logout(request)
    messages.success(request, "Logged Out!")
    return HttpResponseRedirect(reverse('spacefinder:index'))
