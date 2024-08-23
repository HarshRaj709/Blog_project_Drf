from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('BlogApi',views.BlogViewSet,basename='blog')

urlpatterns = [
    path('',views.home,name='home'),
    path('blog/',views.BlogView.as_view(),name='blog'),
    path('blog/<uuid:pk>/',views.BlogView.as_view(), name='blog-detail-update'),
    path('blog/<uuid:pk>/',views.BlogView.as_view(), name='blog-delete'),
    path('blog/',include(router.urls)),

]
