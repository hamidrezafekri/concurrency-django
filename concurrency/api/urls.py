from django.urls import path, include

urlpatterns = [
    path('auth/', include(('concurrency.authentication.urls', 'blog'))),
    path('user/',include(("concurrency.users.urls" , "user"))),
]
