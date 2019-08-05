import re

from django import template
from django.urls import NoReverseMatch, reverse
from Insta.models import Like


register = template.Library()

@register.simple_tag
def is_following(current_user, background_user):
    return background_user.get_followers().filter(creator=current_user).exists()

@register.simple_tag
#in the model like, .objects will return all objects of like
def has_user_liked_post(post, user):
    # if the user has already like your post, show full heart
    try:
        like = Like.objects.get(post=post, user=user)
        return "fa-heart"
    # else, return empty heart
    except:
        return "fa-heart-o"

@register.simple_tag(takes_context=True)
def active(context, pattern_or_urlname):
    try:
        pattern = reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return 'active'
    return ''
