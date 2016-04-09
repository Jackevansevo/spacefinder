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
    context = fetch_index_data()

    if request.user.is_authenticated():
        context['user'] = request.user

    # Check to see if a POST has been submitted
    if request.POST:
        login_form = LoginForm(request.POST)
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if "login" in request.POST:
            # Load the inital form
            if login_form.is_valid():
                user = login_form.login(request)
                if user:
                    login(request, user)
                    thumbs_up_symbol = "<i style='color: #4F844F;' class='fa fa-thumbs-up fa-fw'></i>"
                    messages.success(request, "Logged In! " + thumbs_up_symbol)
                    return redirect(reverse('spacefinder:index'))
            else:
                context['login_form'] = login_form
        elif "register" in request.POST:
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
                messages.success(request, "Registered successfully!")
                return redirect(reverse('spacefinder:index'))
            else:
                print(student_form.errors, user_form.errors)
                context['student_form'] = student_form
                context['user_form'] = user_form
    return render(request, 'spacefinder/index.html', context)


def fetch_index_data():
    """Returns necessary context for the index page"""
    top_voters = Student.objects.annotate(num_ratings=Count('rating')).order_by('-num_ratings')[:6]
    top_voters_json = [[e.user.username, e.num_ratings] for e in top_voters]
    return {
        'study_space_list': StudySpace.objects.order_by('-avg_rating'),
        'top_student_voters': top_voters,
        'top_student_voters_list': top_voters_json,
        'login_form': LoginForm(),
        'user_form': UserForm(),
        'student_form': StudentForm()
    }


def profile(request, slug):
    """Individual user profile page"""
    student = get_object_or_404(Student, slug=slug)
    ratings = Rating.objects.filter(student=student).order_by('timestamp')
    latest_ratings = get_latest_ratings_list(ratings)[-50:]
    average_rating = ratings.aggregate(Avg('rating'))
    rating_streak = len(set([date[0] for date in get_days_ratings(ratings, 3, "%-d")]))
    studyspace_rating_breakdown = ratings.values(
        'studyspace', 'studyspace__space_name'
    ).annotate(num_votes=Count('studyspace')).order_by('-num_votes')[:3]
    context = {
        'login_form': LoginForm(),
        'user_form': UserForm(),
        'student_form': StudentForm(),
        'student': student,
        'ratings': ratings,
        'latest_ratings': latest_ratings,
        'average_rating': average_rating,
        'rating_streak': rating_streak,
        'studyspace_rating_breakdown': studyspace_rating_breakdown
    }
    return render(request, 'spacefinder/profile.html', context)


def studyspace(request, slug):
    """ Page to display detailed information about each studyspace."""
    # Load study space information to pass to the view
    space = get_object_or_404(StudySpace, slug=slug)

    # Load all the ratings associated with this studyspace
    ratings = Rating.objects.filter(studyspace=space).order_by('-timestamp')

    # Get the last 20 votes
    latest_ratings = get_latest_ratings_list(ratings)[-20:]

    # Get votes from the past 24 hours
    days_ratings = get_days_ratings(ratings, 1, "%I:%M%p")

    return render(request, 'spacefinder/studyspace.html', {
        'studyspace': space,
        'latest_ratings': latest_ratings,
        'days_ratings': days_ratings,
    })


def get_latest_ratings_list(ratings):
    """Returns last given number of ratings in ISO 8601 format"""
    return [[timezone.localtime(rating.timestamp).strftime("%I:%M%p"),
             rating.rating] for rating in ratings]


def get_days_ratings(ratings, number_of_days, time_format):
    """Returns array of ratings from specified time frame in desired format"""
    today = timezone.localtime(timezone.now())
    timeframe = today - timedelta(days=number_of_days)
    return [[timezone.localtime(rating.timestamp).strftime(time_format),
             rating.rating] for rating in
            ratings.filter(timestamp__range=[timeframe, today])[::-1]]


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
        time_threshold = current_time - timedelta(hours=0.2)
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
    remaining_time = timedelta(hours=0.2) - time_since_voted
    minutes = str(time.strftime("%-M", time.gmtime(remaining_time.seconds)))
    seconds = str(time.strftime("%-S", time.gmtime(remaining_time.seconds)))
    return minutes, seconds


@login_required
def user_logout(request):
    """Allows users to logout"""
    logout(request)
    logout_synbol = "<i style='color: #4F844F;' class='fa fa-sign-out fa-fw'></i>"
    messages.success(request, "Logged Out! " + logout_synbol)
    return redirect(reverse('spacefinder:index'))
