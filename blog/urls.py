from django.urls import path
from .views import (
    BlogViewset,
    BlogSharingView,
    SharedBlogsListView,
    AuthorsWithAccessView,
)

urlpatterns = [
    path("", BlogViewset.as_view({"get": "list", "post": "create"}), name="blog-list"),
    path("blogs/<str:pk>/", BlogViewset.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="blog-detail"),
    path("share/", BlogSharingView.as_view(), name="share-blog"),
    path("shared-blogs/", SharedBlogsListView.as_view(), name="shared-blogs"),
    path("authors-with-access/", AuthorsWithAccessView.as_view(), name="authors-with-access"),
]

