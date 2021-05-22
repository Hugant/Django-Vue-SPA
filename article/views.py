import json
import os
from datetime import datetime

from django.http import response
from django.shortcuts import render
from rest_framework import viewsets

from article.serializers import ArticleSerializer
from article.utils import Article, Author, ArticlesVirtualManager

avm = ArticlesVirtualManager('settings.xml')


def index(request):
	return render(request, 'index.html')


def articles(request):
	articles = []
	for article in avm.get_articles():
		authors = []
		for author in article.authors:
			authors.append({
				'last_name': author.last_name,
				'first_name': author.first_name,
				'middle_name': author.middle_name
			})
		articles.append({
			'id': article.id,
			'title': article.title,
			'category': article.category,
			'authors': authors,
			'creation_date': datetime.strftime(article.creation_date, '%d-%m-%y'),
			'modified_date': datetime.strftime(article.modified_date, '%d-%m-%y'),
			'text': article.text.strip()
		})

	return response.JsonResponse(json.dumps(articles), safe=False)


def article(request, article_id):
	article = avm.get_article(int(article_id))
	authors = []
	for author in article.authors:
		authors.append({
			'last_name': author.last_name,
			'first_name': author.first_name,
			'middle_name': author.middle_name
		})
	article_json = {
		'id': article.id,
		'title': article.title,
		'category': article.category,
		'authors': authors,
		'creation_date': datetime.strftime(article.creation_date, '%d-%m-%y'),
		'modified_date': datetime.strftime(article.modified_date, '%d-%m-%y'),
		'text': article.text.strip()
	}

	return response.JsonResponse(json.dumps(article_json), safe=False)


def add_article(request):
	data = json.loads(request.body)
	print('data: ' + str(data))
	authors = []
	for author in data['authors']:
		authors.append(Author(author['last_name'], author['first_name'], author['middle_name']))
	article = avm.add_article(data['title'], data['category'], authors , data['text'])
	authors = []
	for author in article.authors:
		authors.append({
			'last_name': author.last_name,
			'first_name': author.first_name,
			'middle_name': author.middle_name
		})
	article_json = {
		'id': article.id,
		'title': article.title,
		'category': article.category,
		'authors': authors,
		'creation_date': datetime.strftime(article.creation_date, '%d-%m-%y'),
		'modified_date': datetime.strftime(article.modified_date, '%d-%m-%y'),
		'text': article.text.strip()
	}

	return response.JsonResponse(json.dumps(article_json), safe=False)


def edit_article(request, article_id):
	data = json.loads(request.body)
	article = avm.get_article(int(article_id))
	article.modify(data['title'], data['category'], data['authors'], data['text'])

	article = avm.get_article(int(article_id))
	authors = []
	for author in article.authors:
		authors.append({
			'last_name': author.last_name,
			'first_name': author.first_name,
			'middle_name': author.middle_name
		})
	article_json = {
		'id': article.id,
		'title': article.title,
		'category': article.category,
		'authors': authors,
		'creation_date': datetime.strftime(article.creation_date, '%d-%m-%y'),
		'modified_date': datetime.strftime(article.modified_date, '%d-%m-%y'),
		'text': article.text.strip()
	}

	return response.JsonResponse(json.dumps(article_json), safe=False)


def delete_article(request, article_id):
	avm.remove_article(article_id)
	return response.JsonResponse(json.dumps([]), safe=False)
