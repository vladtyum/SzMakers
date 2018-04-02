from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^events$', views.all_events, name='events'),
    # url(r'^events/(?P<slug>[-\w]+)/$', views.EventDetailView.as_view(), name='article-detail'),
    # url(r'^events/(?P<slug>[-\w]+)/$', views.EventDetailView.as_view(), name='article-detail'),
    # url(r'^event/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[-\w]+)/$',
    #     views.EventDetailView.as_view(), name='article-detail'),
    url(r'^event/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        views.EventDetailView.as_view(), name='event-detail'),
    url(r'^org/(?P<slug>[-\w]+)/$',
        views.OrgDetailView.as_view(), name='org-detail'),
    url(r'^organizers/$', views.OrgsList.as_view(), name='organizers'),
    url(r'^org-reg/', views.registerOrg, name='org-reg'),
    url(r'^event-reg/', views.eventReg, name='event-reg'),
    url(r'^dashboard/', views.dashboardEventList, name='dashboard'),
    url(r'^account/', views.account , name='account'),
    url(r'^event-edit/(?P<id>[0-9]+)/', views.eventEdit, name='event-edit'),
    url(r'^org-update/', views.orgProfileUpdate, name='org-update'),
]
