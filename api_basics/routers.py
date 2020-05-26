from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('article', views.ArticleViewset, basename='article_viewset')
router.register('generic', views.ArticleGenericViewset, basename='generic_viewset')
