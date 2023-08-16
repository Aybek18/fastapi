from django.urls import path

from lawyer.views import HomeView, HomeEnView, HomeCnView, SuccessPageView, SuccessPageEnView,SuccessPageCnView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("home-en/", HomeEnView.as_view(), name="home-en"),
    path("home-cn/", HomeCnView.as_view(), name="home-cn"),
    path("success", SuccessPageView.as_view(), name="success",),
    path("success-en", SuccessPageEnView.as_view(), name="success-en"),
    path("success-cn", SuccessPageCnView.as_view(), name="success-cn")
]
