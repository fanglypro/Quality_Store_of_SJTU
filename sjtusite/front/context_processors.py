from .models import User, Owner


# html中用户登陆验证
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
