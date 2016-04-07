from .forms import UserForm, StudentForm, LoginForm
from .models import StudySpace, Rating, Student, calc_average
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Avg
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.utils import timezone
import time


def index(request):
    """Shows list of studyspaces, along with corresponding 'busyness' score"""
    # Initialize the context for the index page
    context = fetch_index_context()
    # If the user has made a POST request to login, then fetch any form errors
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.login(request)
            if user:
                login(request, user)
                messages.success(request, "Logged In!")
                return redirect(reverse('spacefinder:index'))
        else:
            context['login_form'] = login_form
    # Else then the user has made a GET request
    if request.user.is_authenticated():
        context['user'] = request.user
    # Don't overwrite the login form if it's already been submitted
    if 'login_form' not in context:
        context['login_form'] = LoginForm()
    # Request Registration forms
    context['user_form'] = UserForm()
    context['student_form'] = StudentForm()
    return render(request, 'spacefinder/index.html', context)


def fetch_index_context():
    """Returns necessary context for the index page"""
    top_student_voters = Student.objects.annotate(
        num_ratings=Count('rating')).order_by('-num_ratings')[:6]
    return {
        'study_space_list': StudySpace.objects.order_by('-avg_rating'),
        'top_student_voters': top_student_voters,
        'top_student_voters_list': [[e.user.username, e.num_ratings] for e in
                                    top_student_voters]
    }


def profile(request, slug):
    """Individual user profile page"""
    student = Student.objects.get(slug=slug)
    ratings = Rating.objects.filter(student=student)
    latest_ratings = get_latest_ratings(ratings, 50)[::-1]
    average_rating = ratings.aggregate(Avg('rating'))
    studyspace_rating_breakdown = ratings.values(
        'studyspace', 'studyspace__space_name'
    ).annotate(num_votes=Count('studyspace')).order_by('-num_votes')[:3]
    return render(request, 'spacefinder/profile.html', {
        'student': student, 'ratings': ratings,
        'latest_ratings': latest_ratings,
        'average_rating': average_rating,
        'studyspace_rating_breakdown': studyspace_rating_breakdown
    })


def studyspace(request, slug):
    """ Page to display detailed information about each studyspace."""
    # Load study space information to pass to the view
    space = get_object_or_404(StudySpace, slug=slug)

    # Load all the ratings associated with this studyspace
    ratings = Rating.objects.filter(studyspace=space).order_by('-timestamp')

    # Get the last 50 votes
    latest_ratings = get_latest_ratings(ratings, 20)

    # Get votes from the past 24 hours
    days_ratings = get_days_ratings(ratings, 1)

    return render(request, 'spacefinder/studyspace.html', {
        'studyspace': space,
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
        student = request.user.student
        # Check if the user has voted recently
        current_time = timezone.localtime(timezone.now())
        time_threshold = current_time - timedelta(hours=0.25)
        # Get the timestamp of the lastest rating in the past 15 minutes
        last_rating = Rating.objects.all().filter(
            student=student, timestamp__gte=time_threshold
        ).order_by('-timestamp').first()
        # If user attempts to vote again within 15 minute window
        if last_rating:
            # Show an error display how long left until can they vote again
            mins, secs = get_time_until_next_vote(current_time, last_rating)
            error_msg = "You've already voted recently! Vote again in: "
            time = mins + " minutes, " + secs + " seconds"
            messages.error(request, error_msg+time)
            return redirect(request.META.get('HTTP_REFERER'))
        # Get a copy of the corresponding studyspace object for that page
        studyspace = get_object_or_404(StudySpace, pk=studyspace_id)
        # Get the value of the users score
        score = request.POST['choice']
        # Update 'busyness' score
        Rating(
            studyspace=studyspace,
            student=student,
            rating=score).save()
        studyspace.save(update_fields=['avg_rating'])
        # Check if the users vote is similar to the last 5 votes
        average = calc_average(studyspace, 0.5, 5)
        if average-1 <= float(score) <= average+1:
            student.karma += 1
            student.save()
        messages.success(request, "Thanks for voting!")
        return redirect(reverse('spacefinder:index'))
    # If user is not authenticated at all
    else:
        messages.error(request, "Must be logged in to vote!")
    # Reload current page + error message if unauthorised user attempts to vote
    return redirect(request.META.get('HTTP_REFERER'))


def get_time_until_next_vote(current_time, last_rating):
    """Returns the amount of time until the user next available vote"""
    time_since_voted = current_time - last_rating.timestamp
    remaining_time = timedelta(hours=0.25) - time_since_voted
    minutes = str(time.strftime("%-M", time.gmtime(remaining_time.seconds)))
    seconds = str(time.strftime("%-S", time.gmtime(remaining_time.seconds)))
    return minutes, seconds


def register(request):
    """Allow new users to Register an account"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
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
    return redirect(reverse('spacefinder:index'))


@login_required
def user_logout(request):
    """Allows users to logout"""
    logout(request)
    messages.success(request, "Logged Out!")
    return redirect(reverse('spacefinder:index'))
