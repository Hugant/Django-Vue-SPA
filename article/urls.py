from django.urls import path

from article import views

urlpatterns = [
	path('', views.index, name='index'),
	path('articles/', views.articles, name='articles'),
	path('articles/add', views.add_article, name='add_article'),
	path('articles/<int:article_id>/', views.article, name='article'),
	path('articles/<int:article_id>/edit', views.edit_article, name='edit_article'),
	path('articles/<int:article_id>/delete', views.delete_article, name='remove_article')
]
