from MalyshevAsk.models import User, Tag, TagManager, UserManager
from MalyshevAsk.forms import LoginForm

def load_tags_and_users_data(request):
    context_data = dict()
    context_data['topUsers'] = User.objects.bestUsers()
    context_data['topTags'] = Tag.objects.bestTags()
    if request.user.is_authenticated():
    	context_data['auth'] = True
    	context_data['user'] = request.user
    else:
    	context_data['auth'] = False
    	context_data['login_form'] = LoginForm()
    return context_data