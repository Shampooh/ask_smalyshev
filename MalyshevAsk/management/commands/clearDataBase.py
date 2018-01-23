from django.core.management.base import BaseCommand, CommandError
from MalyshevAsk.models import User, Question, Answer, Like, Tag

class Command(BaseCommand):
	def handle(self, *args, **options):
		Answer.objects.all().delete()
		Like.objects.all().delete()
		Question.objects.all().delete()
		Tag.objects.all().delete()
		self.stdout.write(self.style.SUCCESS('Data base clear successfully!'))