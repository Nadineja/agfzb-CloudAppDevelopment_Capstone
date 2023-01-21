from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('index', view=views.get_dealerships, name='index'),
    # path for about view
    path('about/', views.about, name='about'),
    # path for dealerships by states
    path(route='state/<str:state>/', view=views.get_dealer_state, name="state_dealers"),
    # path for contact us view
    path('contact/', views.contact, name='contact'),
    # path for registration
    path(route='registration/', view=views.registration_request, name='registration'),
    # path for login
    path(route='login/', view=views.login_request, name='login'),
    # path for logout
    path(route='logout/', view=views.logout_request, name='logout'),
    path(route='index', view=views.index, name='index'),
    # path for dealer reviews view
    path('dealer/<int:id>/', view=views.get_dealer_details, name='dealer_details'),
    # path to retrieve dealer by id
    path(route='dealership/<int:id>/', view=views.get_dealer_id, name='dealer_by_id'),
    # path for add a review view
    path('add_review/<int:id>/', view=views.add_review, name='add_review')




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)