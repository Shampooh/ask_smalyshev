from django.core.management.base import BaseCommand, CommandError
from MalyshevAsk.models import User, Question, Answer, Like, Tag
from loremipsum import get_sentence
from loremipsum import get_paragraph
import random

class Command(BaseCommand):
	def handle(self, *args, **options):
		for i in range(5):
			newUser = User(username = 'TestUser' + str(i))
			newUser.save()
		users = User.objects.all()
		for i in range(10):
			newTag = Tag(text='TestTag' + str(i))
			newTag.save()
		self.stdout.write(self.style.SUCCESS('Generation of test tags completed successfully!'))
		tags = Tag.objects.all()
		for i in range(25):
			upperLine = random.randrange(10)
			bottomLine = upperLine + random.randrange(10 - upperLine) + 1
			newQuestion = Question(asking=users[random.randrange(5)], title=get_sentence(), text=get_paragraph(), ratin=random.randrange(100))
			newQuestion.save()
			for tag in tags[upperLine:bottomLine]:
				newQuestion.tags.add(tag)
		self.stdout.write(self.style.SUCCESS('Generation of test Questions completed successfully!'))
		questions = Question.objects.all()
		for question in questions:
			counter = 0
			for user in users:
				newLike = Like(assessment=(-1 + random.randrange(2) * 2), question_id = question.id, user_id=user.id)
				newLike.save()
				counter+=newLike.assessment
			question.ratin=counter
			question.save()
			for i in range(random.randrange(10)):
				newAnswer = Answer(text=get_paragraph(), correct=False, answerer_id=(users[random.randrange(5)].id), question_id=question.id)
				newAnswer.save()
		self.stdout.write(self.style.SUCCESS('Generation of test Answers and Likes completed successfully!'))
