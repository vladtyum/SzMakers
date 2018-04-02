from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *
from django.contrib.auth.models import User


class MembershipInLine(admin.TabularInline):
    model = Event.dt_event.through
    extra = 1


class EventDateTimeForm(forms.ModelForm):
    class Meta:
        model = EventDateTime
        fields = '__all__'


class EventDateTimeAdmin(admin.ModelAdmin):
    form = EventDateTimeForm
    list_display = ('edate', 'etime')
    inlines = [
        MembershipInLine,
    ]

admin.site.register(EventDateTime, EventDateTimeAdmin)


class EventAdminForm(forms.ModelForm):
    richcontent = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Event
        exclude = ['dt_event']


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'author',)
    normaluser_fields = ['title','title_cn', 'district', 'fee',
                         'location_cn', 'location_en', 'content_en', 'content_cn', 'richcontent', 'is_published', 'thumbnail', 'wechat_qr', 'org']
    superuser_fields = ['author',]
    inlines = [
        MembershipInLine,
    ]
    # prepopulated_fields = {"slug": ("title",)} can not be used since
    # causing conflict for normal user because of slug field closed for him

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.fields = self.normaluser_fields + self.superuser_fields
        else:
            self.fields = self.normaluser_fields
        return super(EventAdmin, self).get_form(request, obj, **kwargs)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return Event.objects.all()
        return Event.objects.filter(author=request.user)

admin.site.register(Event, EventAdmin)


admin.site.register(Org)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
