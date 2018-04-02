from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

from ckeditor_uploader.fields import RichTextUploadingField
from autoslug import AutoSlugField

class Org(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    orgname = models.CharField(max_length=150, null=False, blank=False)
    slug = AutoSlugField(populate_from='orgname',null=True, blank=True, unique=True)
    logo = models.ImageField(upload_to='uploads/org/logos/', null=True, blank=True)
    qr = models.ImageField(upload_to='uploads/org/qrs/', null=True, blank=True )
    location_cn = models.CharField(max_length=200, null=True, blank=True)
    location_en = models.CharField(max_length=200, null=True, blank=True)
    about_en = models.TextField(null=True, blank=True)
    about_cn = models.TextField(null=True, blank=True)
    richcontent = RichTextUploadingField(null=True, blank=True)


    # i guess this block is not needed anymore, since AutoSlug installed
    # but leave it for now, just in a case

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.slug = slugify(self.orgname)
    #         super(Org, self).save(*args, **kwargs)

    def __str__(self):
        return self.orgname

    def get_absolute_url(self):
        return reverse('org-detail', kwargs={'slug': self.slug})


class EventDateTime(models.Model):
    edate = models.DateField()
    etime = models.TimeField()

    def __str__(self):
        return str(self.edate) + ' ' + str(self.etime)


class EventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            start_date=models.Min('dt_event__edate')).order_by('start_date')


class Event(models.Model):
    REGIONS = (
        ('Ns', '南山Nanshan'),
        ('Ft', '福田Futian'),
        ('Lh', '罗湖Luohu'),
        ('Lg', '龙岗Longgang'),
        ('Bn', '宝安Baoan'),
    )
    author = models.ForeignKey(User, null=True, blank=True, related_name="author", on_delete=models.PROTECT)
    org = models.ForeignKey(Org, null=True, blank=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, null=False, blank=False)
    slug = AutoSlugField(populate_from='title',null=True, blank=True, unique=True)
    title_cn = models.CharField(max_length=150, null=True, blank=True)
    dt_event = models.ManyToManyField(EventDateTime, related_name="event")
    district = models.CharField(max_length=2,choices=REGIONS, null=False, blank=False)
    fee = models.DecimalField(max_digits=4, decimal_places=0,null=True, blank=True )
    location_cn = models.CharField(max_length=200, null=True, blank=False)
    location_en = models.CharField(max_length=200, null=True, blank=False)
    content_en = models.TextField(null=True, blank=True)
    content_cn = models.TextField(null=True, blank=True)
    richcontent = RichTextUploadingField(null=True, blank=True)
    is_published = models.BooleanField(null=False, blank=False, default=False)
    thumbnail = models.ImageField('thumbnail', upload_to='uploads/event_thumbnails/', null=True, blank=True)
    wechat_qr= models.ImageField('qr',upload_to='uploads/wechat_qr-s/', null=True, blank=True)
    objects = EventManager()

    class Meta:
        verbose_name_plural = "Events"
    
    # i guess this block is not needed anymore, since AutoSlug installed
    # but leave it for now, just in a case
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.slug = slugify(self.title)
    #     super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug,
                                                 'pk': self.pk,})
