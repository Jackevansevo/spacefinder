from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Avg


class Department(models.Model):
    """Department """
    department_name = models.CharField(max_length=200)

    def __str__(self):
        return self.department_name


class Student(models.Model):
    """Default django user model with additional attributes"""
    user = models.OneToOneField(User, related_name='student')
    slug = models.SlugField(unique=True)
    karma = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        """Auto creates slug field and recalculates avg_rating on save"""
        self.slug = slugify(self.user.username)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class StudySpace(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    space_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    wheelchair_access = models.BooleanField(default=False)
    computer_access = models.BooleanField(default=False)
    avg_rating = models.FloatField(default=3.0)
    opening_time = models.TimeField(default="06:00:00")
    closing_time = models.TimeField(default="18:00:00")

    def save(self, *args, **kwargs):
        """Auto creates slug field and recalculates avg_rating on save"""
        self.slug = slugify(self.space_name)
        results = Rating.objects.filter(studyspace=self.id).order_by('-id')[:1]
        if results.exists():
            average = results.aggregate(Avg('rating')).get('rating__avg')
            self.avg_rating = average
        super(StudySpace, self).save(*args, **kwargs)

    def __str__(self):
        return self.space_name


class Rating(models.Model):
    studyspace = models.ForeignKey(StudySpace, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
