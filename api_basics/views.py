from django.shortcuts import render
from .serializers import ArticleSerializer
from .models import Article
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from rest_framework import generics, mixins

from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets
from django.shortcuts import get_object_or_404


# https://www.youtube.com/watch?v=B38aDwUpcFc
# Create your views here.
# Simple API view
# @csrf_exempt
# def article_list_view(request):
#
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         ser = ArticleSerializer(articles, many=True)
#         return JsonResponse(ser.data, safe=False)
#
#     elif request.method == 'POST':
#         # print(request.data)
#         data = JSONParser().parse(request)
#         ser = ArticleSerializer(data=data)
#
#         if ser.is_valid():
#             ser.save()
#             return JsonResponse(ser.data, status=201)
#         return JsonResponse(ser.errors, status=400)
#
#
# @csrf_exempt
# def article_detail_view(request, pk):
#
#     try:
#         article = Article.objects.get(pk=pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         ser = ArticleSerializer(article)
#         return JsonResponse(ser.data, status=200)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         ser = ArticleSerializer(article, data=data)
#
#         if ser.is_valid():
#             ser.save()
#             return JsonResponse(ser.data, status=200)
#         return JsonResponse(ser.errors, status=400)
#
#     elif request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)


# Function Bases View
@api_view(['GET', 'POST'])
def article_list_view(request):

    if request.method == 'GET':
        articles = Article.objects.all()
        ser = ArticleSerializer(articles, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        ser = ArticleSerializer(data=data)

        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_view(request, pk):
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = ArticleSerializer(article)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = request.data
        ser = ArticleSerializer(article, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Class bases view
class ArticleAPIView(APIView):

    def get(self, request):
        articles = Article.objects.all()
        ser = ArticleSerializer(articles, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        ser = ArticleSerializer(data=data)

        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class AricleDetailsAPIView(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):

        article = self.get_object(pk)
        ser = ArticleSerializer(article)
        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, pk):

        article = self.get_object(pk)
        ser = ArticleSerializer(article, data=request.data)

        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generic view and mixins

class GenericView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    lookup_field = 'pk'

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

    def post(self, request, pk=None):
        return self.create(request)

    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

# Viewset
class ArticleViewset(viewsets.ViewSet):

    def list(self, request):
        articles = Article.objects.all()
        ser = ArticleSerializer(articles, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        ser = ArticleSerializer(article)
        return Response(ser.data, status=status.HTTP_200_OK)

    def create(self, request):

        ser = ArticleSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk=pk)
        data = request.data
        ser = ArticleSerializer(article, data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        queryset = Article.objects.all()
        article = get_object_or_404(queryset, pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Generic ViewSet
class ArticleGenericViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                            mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
