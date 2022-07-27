from django.contrib import admin
from django.urls import path
from shortener.views import (RedirectLink,
                             CreationLinkView,
                             LinksView,
                             DeleteLinkView,
                             DetailLinkView,
                             BulkDeleteLinksView, )

app_name = 'shortener'

urlpatterns = [

    path('creation_link/',  CreationLinkView.as_view(), name='Creation_link'),
    path('delete_links/',  BulkDeleteLinksView.as_view(), name='Delete_links'),
    path('list_link/',  LinksView.as_view(), name='List_link'),
    path('<str:link>/', RedirectLink.as_view(), name='Redirect_link'),
    path('<int:pk>/delete/', DeleteLinkView.as_view(), name='Delete_link'),
    path('<int:pk>/detail/', DetailLinkView.as_view(), name='Detail_link'),
    # path('delete_links/',  BulkDeleteLinksView.as_view(), name='Delete_links'),

]