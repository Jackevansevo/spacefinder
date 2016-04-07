from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone
import hashlib


class Department(models.Model):
    """Department """
    department_name = models.CharField(max_length=200)
    department_icon = models.ImageField()

    def save(self, *args, **kwargs):
        """Auto populates the department icon field"""
        name = slugify(self.department_name)
        self.department_icon = 'department_icons/' + name + '.png'
        super(Department, self).save(*args, **kwargs)

    def __str__(self):
        return self.department_name


class Student(models.Model):
    """Default django user model with additional attributes"""
    user = models.OneToOneField(User, related_name='student')
    slug = models.SlugField(unique=True)
    karma = models.IntegerField(default=0)
    avatar = models.ImageField(
        upload_to='user_avatars', default='user_avatars/default.png'
    )
    # [TODO] Create a checksum field that is created on initial save. Compare
    # checksum against other images to prevent duplciate image upload
    # checksum = models.CharField(unique=True, max_length=16, editable=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Auto creates slug field and recalculates avg_rating on save"""
        self.slug = slugify(self.user.username)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


def md5(fname):
    """Generates checksum for a given file"""
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: fname.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


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
        # Get the latest ten votes from the past half hour
        self.avg_rating = calc_average(self, 0.5, 10)
        super(StudySpace, self).save(*args, **kwargs)

    def __str__(self):
        return self.space_name


def calc_average(_self, time, num_results):
    """Returns average rating for given timeframe / number of votes"""
    time_threshold = timezone.localtime(timezone.now()) - timedelta(hours=time)
    results = Rating.objects.filter(studyspace=_self.id, timestamp__gte=time_threshold)[:num_results]
    if results.exists():
        average = results.aggregate(Avg('rating')).get('rating__avg')
        return average
    return StudySpace._meta.get_field('avg_rating').get_default()


class Rating(models.Model):
    studyspace = models.ForeignKey(StudySpace, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rating = models.IntegerField(default=3)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
