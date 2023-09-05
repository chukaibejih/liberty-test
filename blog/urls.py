from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogViewset,
    BlogSharingView,
    SharedBlogsListView,
    AuthorsWithAccessView,
)

router = DefaultRouter()
router.register("", BlogViewset, basename="blog")


urlpatterns = router.urls + [
    path("share/", BlogSharingView.as_view(), name="share-blog"),
    path("shared-blogs/", SharedBlogsListView.as_view(), name="shared-blogs"),
    path(
        "authors-with-access/",
        AuthorsWithAccessView.as_view(),
        name="authors-with-access",
    ),
]
