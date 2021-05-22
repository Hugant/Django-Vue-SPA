import datetime
import os
import pathlib
import shutil
import xml.etree.ElementTree as xml


class ArticlesVirtualManager:
	def __init__(self, settings_filename):
		self.storage_filepath, self.categories = self.__read_settings(settings_filename)
		self.articles = self.__read_articles()

	@staticmethod
	def __read_settings(settings_filename):
		settings_node = xml.parse(settings_filename).getroot()
		# categories = []
		# for category in settings_node.find('')
		return settings_node.find('workpath').text.strip(), None

	def __read_articles(self):
		article_files = os.listdir(self.storage_filepath)
		articles = []

		for article_file in article_files:
			articles.append(Article(filepath=article_file, storage_filepath=self.storage_filepath))

		return articles

	def get_articles(self):
		return self.articles

	def get_article(self, article_id):
		for article in self.articles:
			if article_id == article.id:
				return article

		raise Exception('Article with id "' + str(article_id) + '" not found')

	def remove_article(self, article_id):
		for article in self.articles:
			if article_id == article.id:
				print(article.id)
				self.articles.remove(article)

				if os.path.isfile(self.storage_filepath + str(article_id) + '_article.xml'):
					os.remove(self.storage_filepath + str(article_id) + '_article.xml')
				else:
					raise Exception('File not found')
				return
		else:
			raise Exception('Article with id ' + str(article_id) + ' not found')

	def update_article(self, article_id, title, category, authors, text):
		for article in self.articles:
			if article.id == article_id:
				article.modify(title, category, authors, text)
				return
		else:
			raise Exception('Article with id ' + str(article_id) + ' not found')

	def add_article(self, title, category, authors, text):
		article = Article(title=title, category=category, authors=authors, text=text,
																 storage_filepath=self.storage_filepath)
		self.articles.append(article)
		return article


class Article:
	def __init__(self, storage_filepath, filepath=None, title=None, category=None, authors=None, text=''):
		self.storage_filepath = storage_filepath
		if filepath is not None:
			self.id, self.title, self.category, self.authors, self.creation_date, \
			self.modified_date, self.text = self.parse_xml(filepath)
		else:
			self.id = None
			self.title = title
			self.category = category
			self.authors = authors
			self.creation_date = datetime.datetime.now()
			self.modified_date = datetime.datetime.now()
			self.text = text

			self.create_article_file()

	def parse_xml(self, filepath):
		root = xml.ElementTree(file=self.storage_filepath + filepath).getroot()
		title = root.find('title').text.strip()
		article_id = int(filepath[:filepath.index('_article.xml')])
		print(article_id)
		category = root.find('category').text.strip()
		authors_node = root.find('authors')
		authors = []
		for author in authors_node.iter('item'):
			text = author.text.strip()
			if text != '':
				author = author.text.strip().split(' ')
				authors.append(Author(author[0], author[1], author[2]))

		date = root.find('date').text.split('/')
		creation_date = datetime.datetime.strptime(date[0].strip(), '%d-%m-%y')
		modified_date = datetime.datetime.strptime(date[1].strip(), '%d-%m-%y')
		text = root.find('text').text

		return article_id, title, category, authors, creation_date, modified_date, text

	def create_article_file(self):
		root = xml.Element('doc')

		self.id = hash(self)
		print(self.id)
		title_node = xml.SubElement(root, 'title')
		title_node.set('auto', 'true')
		title_node.set('type', 'str')
		title_node.set('verify', 'true')
		root.text = '\n\t'
		title_node.text = '\n\t\t' + self.title + '\n\t'
		title_node.tail = '\n'

		category_node = xml.SubElement(root, 'category')
		category_node.set('auto', 'true')
		category_node.set('type', 'str')
		category_node.set('verify', 'true')
		root[0].tail = '\n\t'
		category_node.text = '\n\t\t' + self.category + '\n\t'
		category_node.tail = '\n\t'

		authors_node = xml.SubElement(root, 'authors')
		authors_node.set('auto', 'true')
		authors_node.set('type', 'list')
		authors_node.set('verify', 'true')
		root[1].tail = '\n\t'
		authors_node.text = '\n\t\t'
		authors_node.tail = '\n'

		for author, i in zip(self.authors, range(len(self.authors))):
			print(author)
			author_node = xml.SubElement(authors_node, 'item')
			author_node.set('type', 'str')
			authors_node[i].tail = '\n\t\t\t'
			author_node.text = '\n\t\t\t' + author.last_name + ' ' + author.first_name + ' ' + \
												 author.middle_name + '\n\t\t'
			if i < len(self.authors) - 1:
				author_node.tail = '\n\t\t'
			else:
				author_node.tail = '\n\t'

		date_node = xml.SubElement(root, 'date')
		date_node.set('auto', 'true')
		date_node.set('type', 'str')
		date_node.set('verify', 'true')
		root[2].tail = '\n\t'
		date_node.text = '\n\t\t' + self.creation_date.strftime('%d-%m-%y') + ' / ' + \
										 self.modified_date.strftime('%d-%m-%y') + '\n\t'

		text_node = xml.SubElement(root, 'text')
		text_node.set('auto', 'true')
		text_node.set('type', 'str')
		text_node.set('verify', 'true')
		root[3].tail = '\n\t'
		text_node.text = '\n\t\t' + self.text + '\n\t'
		text_node.tail = '\n'

		tree = xml.ElementTree(root)
		if self.storage_filepath is None:
			tree.write(str(self.id) + '_article.xml', encoding='utf-8')
		else:
			tree.write(self.storage_filepath + str(self.id) + '_article.xml', encoding='utf-8')
		print(self.id)

	def modify(self, title, category, authors, text):
		self.title = title
		self.category = category
		self.authors = authors
		self.text = text
		self.modified_date = datetime.datetime.now()
		self.modify_article_file()

	def modify_article_file(self):
		root = xml.ElementTree(file=self.storage_filepath + str(self.id) + '_article.xml').getroot()
		root.find('title').text = '\n\t\t' + self.title + '\n\t'
		root.find('category').text = '\n\t\t' + self.category + '\n\t'
		root.find('authors').clear()
		authors_node = root.find('authors')
		authors_node.tail = '\n\t'
		authors_node.text = '\n\t\t'
		for author, i in zip(self.authors, range(len(self.authors))):
			author_node = xml.SubElement(authors_node, 'item')
			author_node.set('type', 'str')
			authors_node[i].tail = '\n\t\t\t'
			author_node.text = '\n\t\t\t' + author.last_name + ' ' + author.first_name + ' ' + \
												 author.middle_name + '\n\t\t'
			if i < len(self.authors) - 1:
				author_node.tail = '\n\t\t'
			else:
				author_node.tail = '\n\t'
		root.find('date').text = '\n\t\t' + self.creation_date.strftime('%d-%m-%y') + ' / ' + \
														 self.modified_date.strftime('%d-%m-%y') + '\n\t'
		root.find('text').text = '\n\t\t' + self.text + '\n\t'

		tree = xml.ElementTree(root)
		tree.write(self.storage_filepath + str(self.id) + '_article.xml', encoding='utf-8')
		print(self.id)

	def __hash__(self):
		h = 1030
		for c in self.title:
			h = 101 * h + ord(c) + self.creation_date.timestamp()
		return int(str(int(h))[:12])



class Author:
	def __init__(self, last_name, first_name, middle_name):
		self.first_name = first_name.strip().capitalize()
		self.last_name = last_name.strip().capitalize()
		self.middle_name = middle_name.strip().capitalize()

	def __str__(self):
		return self.last_name + ' ' + self.first_name[0] + '. ' + self.middle_name[0] + '.'
