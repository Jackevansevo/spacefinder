from .forms import UserForm, StudentForm, LoginForm
from .models import StudySpace, Rating, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from datetime import datetime, timedelta
from django.utils import timezone


def index(request):
    """Shows list of studyspaces, along with corresponding 'busyness' score"""

    # Load information to pass to the view
    context = {
        'study_space_list': StudySpace.objects.order_by('-avg_rating')
    }

    # If the user is logged in then we need to fetch their student details
    if request.user.is_authenticated():
        context['user'] = request.user
    else:
        context['login_form'] = LoginForm(auto_id=False)
        context['user_form'] = UserForm()
        context['student_form'] = StudentForm()
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
    spaceName = get_object_or_404(StudySpace, slug=slug)

    # Load all the ratings associated with this studyspace
    ratings = Rating.objects.filter(studyspace=spaceName).order_by('-timestamp')

    # Get the last 50 votes
    latest_ratings = get_latest_ratings(ratings, 20)

    # Get votes from the past 24 hours
    days_ratings = get_days_ratings(ratings, 1)

    return render(request, 'spacefinder/detail.html', {
        'studyspace': spaceName,
        'latest_ratings': latest_ratings,
        'days_ratings': days_ratings,
    })


def get_latest_ratings(ratings, number):
    """Returns last given number of ratings in ISO 8601 format"""
    return [[timezone.localtime(rating.timestamp).strftime("%I:%M%p"),
             rating.rating] for rating in ratings[:number][::-1]]


def get_days_ratings(ratings, number_of_days):
    """Returns an array of ratings from the past 24 hours in ISO 8601 format"""
    today = timezone.localtime(timezone.now())
    yesterday = today - timedelta(days=number_of_days)
    return [[timezone.localtime(rating.timestamp).strftime("%I:%M%p"),
             rating.rating] for rating in
            ratings.filter(timestamp__range=[yesterday, today])[::-1]]


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
