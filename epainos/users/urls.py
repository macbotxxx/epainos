from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view
from .views import dashboard_index
from .views import contestant_view
from .views import vote_submit
from .views import payment

from . import views

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("upload/", view=dashboard_index, name="dash_index"),
    path("vote/", view=vote_submit, name="vote_submit"),
    path("payment/", view=payment, name="payment"),

    path("upload-contestant/", views.contestant_upload, name="contestant_upload"),
    path("contestant-list/", views.contestant_list, name="contestant_list"),
    path("<str:pk>/contestant-update/", views.update_contestant_profile, name="update_contestant_profile"),
    path("<str:pk>/contestant-delete/", views.delete_contestant_record, name="delete_contestant_record"),
    path("verify/", views.payment_verify, name="payment_verify"),
    path("contestant-vote-list/", views.contestant_vote_list, name="contestant_vote_list"),
    path("transaction-list/", views.transaction_list, name="transaction_list"),

]
