from django.urls import path, include

urlpatterns = [
    path('auth/', include(('concurrency.authentication.urls', 'auth'))),
    path('user/',include(("concurrency.users.urls" , "user"))),
    path('credit/' , include(("concurrency.credit.urls" ,"credit"))),
]
