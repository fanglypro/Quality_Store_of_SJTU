#encoding: utf-8
from .models import User, Owner

def front_user(request):
    user_id = request.session.get('user_id')
    context = {}
    if user_id:
        try:
            user = User.objects.get(pk=user_id)
            context['front_user'] = user
        except:
            pass
    owner_id = request.session.get('owner_id')
    if owner_id:
        try:
            owner = Owner.objects.get(pk=owner_id)
            context['front_owner'] = owner
            context['shopname'] = Owner.objects.get(pk=owner_id).shopname
        except:
            pass
    return context



##没有注册