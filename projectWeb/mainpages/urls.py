from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.index, name='index'),
    url(r'^single_prediction',views.single_prediction, name='single_prediction'),
    url(r'^batch_prediction',views.batch_prediction, name='batch_prediction'),
    url(r'^model_selection',views.model_selection, name='model_selection'),
    url(r'^reBuild_model',views.reBuild_model, name='reBuild_model'),


    #Action
    url(r'^single_action$',views.single_action, name='single_action'),
    url(r'^map_action',views.map_action, name='map_action'),


]