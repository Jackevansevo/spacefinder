from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import StudySpace, Rating, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, StudentForm, LoginForm
from django.contrib.auth.decorators import login_required


def index(request):
    """Shows list of studyspaces, along with corresponding 'busyness' score"""
    # Sort by average 'busyness' score
    study_space_list = StudySpace.objects.order_by('-avg_rating')

    # Load registration form details
    user_form = UserForm()
    student_form = StudentForm()
    login_form = LoginForm(auto_id=False)

    # Load information to pass to the view
    context = {
        'study_space_list': study_space_list,
        'user_form': user_form,
        'student_form': student_form,
        'login_form': login_form,
    }

    # If the user is logged in then we need to fetch their student details
    if request.user.is_authenticated():
        context['user'] = request.user

    return render(request, 'spacefinder/index.html', context)


def profile(request, slug):
    """Individual user profile page"""
    student = request.user.student
    context = {'student': student}
    ratings = Rating.objects.filter(student=student)
    if ratings:
        context['ratings'] = ratings
    return render(request, 'spacefinder/profile.html', context)


def detail(request, slug):
    """ Page to display detailed information about each studyspace."""
    # Load study space information to pass to the view
    studyspace = get_object_or_404(StudySpace, slug=slug)
    ratings = Rating.objects.filter(studyspace=studyspace)
    context = {'studyspace': studyspace, 'ratings': ratings}
    return render(request, 'spacefinder/detail.html', context)


def vote(request, studyspace_id):
    """ Creates a new rating record when the vote button is pressed."""
    if request.user.is_authenticated():
        # Get a copy of the corresponding studyspace object for that page
        studyspace = get_object_or_404(StudySpace, pk=studyspace_id)
        try:
            # Get the value of the users score
            score = request.POST['choice']
        except (KeyError, StudySpace.DoesNotExist):
            # Redisplay the voting form
            return render(request, 'spacefinder/detail.html', {
                'studyspace': studyspace,
                'error_message': "Error when voting.",
            })
        else:
            # Update 'busyness' score
            Rating(
                studyspace=studyspace,
                student=request.user.student,
                rating=score).save()
            studyspace.save(update_fields=['avg_rating'])
            return HttpResponseRedirect(reverse('spacefinder:index'))
    return HttpResponseRedirect(reverse('spacefinder:index'))


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
