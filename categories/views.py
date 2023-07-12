from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Category
from .serializers import CategorySerializer


@api_view(["GET", "POST"])
def categories(request):
    # Category.objects.all() 는 Json이 아니라 Django 모델임. Json 형태로 바꿔줘야 함.
    # 그게 바로 Serializers임.
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        # user로부터 데이터를 가져오고 싶으면 data를 CategorySerializer에게 넘겨라
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data)
        else:
            return Response(serializer.errors)


@api_view(["GET", "PUT"])
def category(request, pk):
    # Django에서 JSON으로 번역하고 싶으면 CategorySerializer에 category를 넘기고
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound
    
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            # 여기서 save를 하면 create를 하지 않는다.
            # db에서 가져온 category와 유저로 받은 데이터가 있기 때문에
            # 즉, 업데이트라고 판단함.
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)
