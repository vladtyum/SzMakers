from django.http import HttpResponse, HttpResponseRedirect, Http404,HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from django.forms.formsets import formset_factory

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import OrgForm, EventForm, EventDTForm, EventUpdateForm, \
    OrgUpdateForm, EventDTFormSet

def index(request):
    user = request.user
    org=None
    try:
        org = Org.objects.get(user_id=request.user.id)
    except Exception:
        pass
    upcoming_events = Event.objects.filter(is_published=True, start_date__gte=timezone.now()).order_by('start_date')
    past_events = Event.objects.filter(is_published=True, start_date__lt=timezone.now()).order_by('-start_date')

    return render(request, 'core/index.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'user': user,
        'org': org,
    })


def about(request):
    return render(request, 'core/about.html', {})


def contact(request):
    return render(request, 'core/contact.html', {})


def register_temp(request):
    return render(request, 'core/register_temp.html', {})


def all_events(request):

    upcoming_events = Event.objects.filter(is_published=True, start_date__gte=timezone.now()).order_by('start_date')
    past_events = Event.objects.filter(is_published=True, start_date__lt=timezone.now()).order_by('-start_date')

    return render(request, 'core/events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })


class EventDetailView(DetailView):

    model = Event

    def event_detail_view_func(request, slug):
        event = Event.objects.get(slug=slug)
        context_dict = {
            'event':event
        }
        return render(request, 'core/event_detail.html', context_dict)


class OrgDetailView(DetailView):

    model = Org

    def org_detail_view_func(request, slug):
        org = Org.objects.get(slug=slug)
        context_dict = {
            'org': org
        }
        return render(request, 'core/org_detail.html', context_dict)


class OrgsList(ListView):
    model = Org
    context_object_name = 'orgs'
    template_name = 'organizers.html'


@login_required
def registerOrg(request):
    if request.user.groups.filter(name='Organizers').exists():
        return HttpResponseNotFound("You are already an organizer") 
    else:
        if request.method == "POST":
            org_form = OrgForm(data=request.POST)
            if org_form.is_valid():
                org = org_form.save(commit=False)
                org.user = request.user
                org.save()
                g = Group.objects.get(name='Organizers') 
                g.user_set.add(request.user)
                return HttpResponseRedirect(reverse('org-update'))
                # else:
                #     return HttpResponse("No website")
            else:
                print(org_form.errors)
        else:
            org_form = OrgForm()
        return render(request, 'core/org-reg.html', {
                            'org_form': org_form,
                            })


@login_required
def eventReg(request):
    #ToDo should be done with property
    if request.user.groups.filter(name="Organizers").exists(): # <<<
        event_form = EventForm()
        DTFormSet = formset_factory(EventDTForm, formset=EventDTFormSet)
        if request.method == "POST":
            event_form = EventForm(request.POST or None, request.FILES or None)
            if event_form.is_valid():
                dt_form = DTFormSet(request.POST or None)
                if dt_form.is_valid():
                    event = event_form.save(commit=False)
                    event.author = request.user
                    event.org = Org.objects.get(user_id=request.user.id)
                    event.thumbnail = event_form.cleaned_data['thumbnail']
                    event.wechat_qr = event_form.cleaned_data['wechat_qr']
                    event.save()
                    for dt in dt_form:
                        edate = dt.cleaned_data.get('edate')
                        etime = dt.cleaned_data.get('etime')
                        item = EventDateTime(edate=edate, etime=etime)
                        item.save()
                        event.dt_event.add(item)
                    event.save()
                    return HttpResponseRedirect(reverse("dashboard"))
                else:
                    dt_formset = DTFormSet()
                    print(dt_form.errors)
            else:
                dt_formset = DTFormSet()
                print(event_form.errors)
        else:
            dt_formset = DTFormSet()
        return render(request, 'core/event-reg.html',
                      {'event_form': event_form, 'dt_formset': dt_formset})
    else:
        return HttpResponse(
            "You are not the organizer yet.\
            Please go to Account >> Org Register"
            )

@login_required
def dashboardEventList(request):
    user = request.user
    events = Event.objects.filter(author=request.user) #self.rquest.user
    return render (request, 'core/dashboard.html',
                             {"events":events,})

@login_required
def account(request):
    is_org = False
    try:
        current_org = Org.objects.get(user_id=request.user.id)
    except Exception:
        pass
    if request.user.groups.filter(name="Organizers").exists():
        is_org = True
    return render (request, 'core/account.html',locals())

@login_required
def eventEdit(request, id):
    event = get_object_or_404(Event, id=id)
    if event.author == request.user:
        DTFormSet = formset_factory(EventDTForm, formset=EventDTFormSet,
                                    extra=0, min_num=1)
        data = [{'edate': item.edate, 'etime': item.etime}
                for item in EventDateTime.objects.filter(event=event)]
        form = EventUpdateForm(request.POST or None, request.FILES or None, instance=event)
        dt_form = DTFormSet(request.POST or None, initial=data)
        if form.is_valid() and dt_form.is_valid():
            form.save()
            old_dt = EventDateTime.objects.filter(event=event)
            n_dt = len(old_dt)
            i = 0
            new_dt = False
            for dt in dt_form:
                edate = dt.cleaned_data.get('edate')
                etime = dt.cleaned_data.get('etime')
                if i < n_dt:
                    old_dt[i].edate = edate
                    old_dt[i].etime = etime
                    old_dt[i].save()
                    i += 1
                else:
                    item = EventDateTime(edate=edate, etime=etime)
                    item.save()
                    event.dt_event.add(item)
                    new_dt = True
            for j in range(n_dt-1, i-1, -1):
                EventDateTime.objects.filter(pk=old_dt[j].pk).delete()
                new_dt = True
            if new_dt:
                event.save()
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            print(form.errors)
        return render(request, 'core/event-edit.html', {
                                'form': form, 'dt_formset': dt_form })
    else:
        return HttpResponseNotFound("\
            <h1>Page not found</h1>\
            <p>Event doesn't exist, or you are not the authour of it</p>\
            <p>Meanwile if you are the author, please contact support</p>"\
            )


@login_required
def orgProfileUpdate(request):
    org = get_object_or_404(Org, id= Org.objects.get(user=request.user).id)
    if request.user.groups.filter(name="Organizers").exists():
        org_form = OrgUpdateForm(request.POST or None, request.FILES or None, instance=org)
        if org_form.is_valid():
            org_v = org_form.save(commit=False)
            org_v.logo = org_form.cleaned_data['logo'] 
            org_v.qr = org_form.cleaned_data['qr']
            org_v.save()
            return HttpResponseRedirect(reverse('account'))
        else:
            print(org_form.errors)
            return render (request, 'core/org_update.html',
                                     {"org_form":org_form,
                                     })
    else:
        return HttpResponse(
            "You are not the organizer yet.\
            Please go to Account >> Org Register"
            )
 
