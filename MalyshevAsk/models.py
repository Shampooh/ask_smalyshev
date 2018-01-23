# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.db.models import Count

class QuestionManager(models.Manager):
	def sortByDate(self):
		objects_list = []
		questions = self.order_by('-date')
		for question in questions:
			list_element = question
			list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
			objects_list.append(list_element)
		return objects_list

	def bestQuestions(self):
		objects_list = []
		questions = self.order_by('-ratin')
		for question in questions:
			list_element = question
			list_element.answers_count = Answer.objects.filter(question_id=question.id).count()
			objects_list.append(list_element)
		return objects_list

	def questionsByTag(self, tag):
		return Question.objects.filter(tags__text = tag)

class UserM(UserManager):
	def bestUsers(self):
		return  User.objects.annotate(total = Count('author')).order_by("-total")[:5]
		"""
		from django.db import connection
		cursor = connection.cursor()
		cursor.execute("""
		"""
			SELECT user.nick, COUNT(*) as count 
			FROM Malyshevask_user user,Malyshevask_answer answers 
			WHERE user.id = answers.answerer_id 
			GROUP BY user.id 
			ORDER BY count DESC)
		
		user_list = []
		for row in cursor.fetchall()[:5]:
			user = self.model(nick = row[0])
			user_list.append(user)
		"""

class AnswerManager(models.Manager):
	def answersOnQuestion(self, id):
		return Answer.objects.filter(question_id=id)

class TagManager(models.Manager):
	def bestTags(self):
		return Tag.objects.annotate(total = Count('tags')).order_by("-total")[:5]

# Create your models here.
class User(AbstractUser):
	avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', default='uploads/noAvatar.png')
	nick = models.CharField(max_length=20)
	objects = UserM()

class Tag(models.Model):
	text = models.CharField(max_length=200)
	objects = TagManager()
	def __unicode__(self):
		return self.text

class Question(models.Model):
	asking = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
	title = models.CharField(max_length=200)
	text = models.CharField(max_length=200)  # найти тип данных побольше!
	ratin = models.IntegerField()
	tags = models.ManyToManyField(Tag, related_name="tags")
	date = models.DateTimeField(default=timezone.now)
	objects = QuestionManager()

class Answer(models.Model):
	answerer = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=200) # найти тип данных побольше!
	correct = models.BooleanField()
	date = models.DateTimeField(default=timezone.now)
	objects = AnswerManager()

class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	assessment = models.SmallIntegerField();
	date = models.DateTimeField(auto_now=True)