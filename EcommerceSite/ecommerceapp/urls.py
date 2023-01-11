from django.urls import path
from .views import accountsCustomerUserCreationView, accountsSellerUserCreationView, \
	accountsEmailPasswordLoginGenericsView, productdetails, Reviews, singleitem

urlpatterns = [

		path('customer-register/', accountsCustomerUserCreationView.as_view(), name='customerCreationURL'),
		path('seller-register/', accountsSellerUserCreationView.as_view(), name='sellerCreationURL'),
		path('user-login/', accountsEmailPasswordLoginGenericsView.as_view(), name='userLoginURL'),
		path("product/",productdetails.as_view(),name="ProductdetailsURL"),
		path("productdelete/<int:id>",productdetails.as_view(),name="ProductdeleteURL"),
		path("reviews/",Reviews.as_view(),name="ReviewsURL"),
		path("reviews/<int:productid>",Reviews.as_view(),name="GetsingleproductreviewsURL"),
		path("get_single_item_details_reviews/",singleitem.as_view(),name="GetsingleproductDetailsRatingsandReviewsURL")
    ]