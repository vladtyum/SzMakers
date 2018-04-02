from django import forms
from django.contrib.auth.models import User
from .models import Org, Event, EventDateTime
from django.contrib.admin.widgets import AdminDateWidget
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Layout, Fieldset
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class OrgForm(forms.ModelForm):
    about_en = forms.CharField(
                    help_text='<i>short inro about organizer </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    about_cn = forms.CharField(
                    help_text='<i>项目介绍 </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    richcontent = forms.CharField(
                    widget=CKEditorUploadingWidget(attrs={'cols':50,'rows': 3}),
                    help_text="""^^^ more details about your project,
                    put pictures, tables,
                    files whatever you want for introducing your project"""
                    )

    class Meta:
        model = Org
        widgets = {'user': forms.HiddenInput()}
        exclude = ['slug', 'logo', 'qr']

    # user = models.ForeignKey(User, null=True, blank=True) 
    # orgname = models.CharField(max_length=150, null=False, blank=False)
    # slug = models.SlugField(max_length=150, unique=True, verbose_name='slug', null=True, blank=True)
    # logo = models.ImageField(upload_to='uploads/org/logos/', null=True, blank=True)
    # qr = models.ImageField(upload_to='uploads/org/qrs/', null=True, blank=True )
    # moto = models.CharField(max_length=200, null=True, blank=True)
    # location_cn = models.CharField(max_length=200, null=True, blank=True)
    # location_en = models.CharField(max_length=200, null=True, blank=True)


class EventDTForm(forms.ModelForm):
    edate = forms.DateField(widget=forms.SelectDateWidget(), label="Date",)
    etime = forms.TimeField(
        widget=forms.TextInput(attrs={'size': 5}),
        initial="19:11",
        help_text='<i> "hh:mm" format</i>',
        label="Time")

    class Meta:
        model = EventDateTime

        fields = ("__all__")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button('remove', 'Remove',
                                     css_class='btn btn-remove'))
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Date and time', 'edate', 'etime', css_class='dt_fieldset ')
        )


class EventDTFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        data = []
        for form in self.forms:
            if form.cleaned_data:
               data.append(form.cleaned_data)
        return data


class EventForm(forms.ModelForm):
    #sectors
    fee = forms.DecimalField(
                    initial=None,
                    help_text='<i>if event is Free, paste 0 </i>',)
    content_en = forms.CharField(
                    help_text='<i>short info for notifications ans stuff </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    content_cn = forms.CharField(
                    help_text='<i>in CN , short info for notifications ans stuff </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    richcontent = forms.CharField(widget=CKEditorWidget(attrs={'cols':50,'rows': 3}))

    class Meta:
        model = Event
        widgets = {'author': forms.HiddenInput(),
                    'org': forms.HiddenInput(),
                    }
        
        #fields = ("__all__")
        exclude = ['dt_event']
    
    # i guess this block is not needed anymore, since AutoSlug installed
    # but leave it for now, just in a case
    # def clean_slug(self):
    #         data = self.cleaned_data['slug']
    #         if Event.objects.filter(slug=data).exists():
    #             raise ValidationError("this slug exists")
    #         return data


class EventUpdateForm(forms.ModelForm):
    #sectors
    fee = forms.DecimalField(
                    initial=None,
                    help_text='<i>if event is Free, paste 0 </i>',)
    content_en = forms.CharField(
                    help_text='<i>short info for notifications ans stuff </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    content_cn = forms.CharField(
                    help_text='<i>in CN , short info for notifications ans stuff </i>', 
                    widget=forms.Textarea(attrs={'rows': 3}))
    richcontent = forms.CharField(widget=CKEditorWidget(attrs={'cols':50,'rows': 3}))

    class Meta:
        model = Event
        widgets = {'author': forms.HiddenInput(),
                    'org': forms.HiddenInput(),
                    }
        
        exclude = ['dt_event']


class OrgUpdateForm(forms.ModelForm):
    orgname = forms.CharField(disabled=True)
    about_en = forms.CharField(help_text='<i>short info about organizer </i>',
        widget=forms.Textarea(attrs={'rows': 3}))
    about_cn = forms.CharField(help_text='<i>short info about organizer </i>',
        widget=forms.Textarea(attrs={'rows': 3}))
    logo = forms.ImageField(help_text='<i>upload your Organizer logo </i>',)
    qr = forms.ImageField(help_text='<i> WeChat QRcode to contact you</i>',)
    class Meta:
        model = Org
        exclude = ['user']
