from rest_framework import status, generics
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK,HTTP_400_BAD_REQUEST

from .models import Items, User, productsUserReviewModel
from .serializers import accountsCustomerCreationSerializer, accountsSellerCreationSerializer, \
    accountEmailLoginSerializer, productserializer, reviewserializer


# Customer User Creation
class accountsCustomerUserCreationView(generics.CreateAPIView):
    serializer_class = accountsCustomerCreationSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        serializer = accountsCustomerCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Seller User Creation
class accountsSellerUserCreationView(generics.CreateAPIView):
    serializer_class = accountsSellerCreationSerializer
    queryset = get_user_model().objects.all()

    def post(self, request, *args, **kwargs):
        serializer = accountsSellerCreationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# User LogIn Views
class accountsEmailPasswordLoginGenericsView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = accountEmailLoginSerializer
    pagination_class = None

    def post(self, request):
        serializer = accountEmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class productdetails(APIView):
    def post(self,request):
        if request.user.is_seller ==True:
            serializer = productserializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("{message:Product created}",status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response("{message:You have no seller permission}")
    def get(self,request):
        if request.user.is_seller == True:
            try:
                products= Items.objects.all().filter(seller_id=request.user_id)
            except:
                return Response("{message:No products found}",status=HTTP_404_NOT_FOUND)
            serializer = productserializer(products,many=True)
        if request.user.is_customer ==True:
            try:
                products= Items.objects.all()
            except:
                return Response("{message:No products found}",status=HTTP_404_NOT_FOUND)
            serializer = productserializer(products,many=True)
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
    def delete(self,request,id):
        if request.user.is_seller == True:
            try:
                product = Items.objects.get(id=id,seller_id=request.user_id)
            except:
                return Response("{message:Product doesnt exist}")
            product.delete()
            return Response("{message:Product delete successful}",status=HTTP_200_OK)
        else:
            return Response("{message:You dont have seller permission}",status=HTTP_400_BAD_REQUEST)
class Reviews(APIView):
    def get(self, request):
        r=productsUserReviewModel.objects.all()
        reviews = reviewserializer(r,many=True)
        if reviews.is_valid():
            return Response(reviews.data,status=HTTP_200_OK)
        else:
            return Response(reviews.errors,status=HTTP_400_BAD_REQUEST)
    def post(self,request,productid):
        if request.user.is_customer==True:
            review = reviewserializer(data = request.data,user_id=request.user_id,product_id =productid)
            if review.is_valid():
                review.save()
                return Response(review.data,status=HTTP_201_CREATED)
            else:
                return Response(review.errors,status = HTTP_400_BAD_REQUEST)
        else:
            return Response("{message:You are not a customer}")
class singleitem(APIView):
    def get(self,request,proid):
        if request.user.is_customer==True or request.user.is_seller==True:
            try:
                object = productsUserReviewModel.objects.get(product_id=proid)
            except:
                return Response("{message:Product not found}")
            review = reviewserializer(object)
            if(review.is_valid()):
                return Response(review.data,status=HTTP_200_OK)
            else:
                return Response(review.errors,status=HTTP_400_BAD_REQUEST)

