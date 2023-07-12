from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Category
from .serializers import CategorySerializer


class Categories(APIView):
    def get(self, request):
        # Category.objects.all() 는 Json이 아니라 Django 모델임. Json 형태로 바꿔줘야 함.
        # 그게 바로 Serializers임.
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,  # 데이터가 여러 개이면 True로 설정
        )
        return Response(serializer.data)

    def post(self, request):
        # user로부터 데이터를 가져오고 싶으면 data를 CategorySerializer에게 넘겨라
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        serializer = CategorySerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)
