from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer


@api_view()
def categories(request):
    # Category.objects.all() 는 Json이 아니라 Django 모델임. Json 형태로 바꿔줘야 함.
    # 그게 바로 Serializers임.
    all_categories = Category.objects.all()
    serializer = CategorySerializer(all_categories, many=True)
    return Response(
        {
            "ok": True,
            "categories": serializer.data,
        }
    )
