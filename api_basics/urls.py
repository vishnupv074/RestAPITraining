from django.contrib import admin
from django.urls import path,include
from . import views
from . import routers


urlpatterns = [
    path('article/', views.article_list_view),
    path('article/<int:pk>', views.article_detail_view),
    path('posts/', views.ArticleAPIView.as_view()),
    path('posts/<int:pk>', views.AricleDetailsAPIView.as_view()),
    path('generic/<int:pk>', views.GenericView.as_view()),
    path('generic/', views.GenericView.as_view()),
    path('viewset/', include(routers.router.urls))
]