from django import template
from django.contrib.auth.models import Group
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    print('group',group)
    print('user',user)
    try:
        if group in user.groups.all():
            print('True')
            return True
    except:
        # if group =="customer":
        #     print('False')
        #     return True
        return False
    #
    # print(user.groups.all())
    # return True if group in user.groups.all() else False