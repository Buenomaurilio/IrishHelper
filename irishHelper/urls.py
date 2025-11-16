from catalog.api_views import ResourceList
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from catalog.views import irish_helper, track_click, home_redirect

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # /i18n/setlang/
    path("", home_redirect, name="home"),
    path("<str:locale>/<str:country>/", irish_helper, name="irishhelper"),
    path("track/click/<int:link_id>/", track_click, name="track_click"),
    path("api/v1/resources", ResourceList.as_view(), name="api_resources"),
]


# from django.urls import path

# urlpatterns += [
#     path("api/v1/resources", ResourceList.as_view(), name="api_resources"),
# ]

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", irish_helper, name="irishhelper_default"),
#     path("<str:locale>/<str:country>/", irish_helper, name="irishhelper"),
#     path("track/click/<int:link_id>/", track_click, name="track_click"),
# ]
# from django.contrib import admin
# from django.urls import path
# from catalog.views import irish_helper, track_click, home_redirect


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", home_redirect, name="home"),
#     path("<str:locale>/<str:country>/", irish_helper, name="irishhelper"),
#     path("track/click/<int:link_id>/", track_click, name="track_click"),
# ]
