from django import template

register = template.Library()


@register.filter
def display_name(user):
    if not user or not getattr(user, "is_authenticated", False):
        return "Guest"
    full_name = (user.get_full_name() or "").strip()
    if full_name:
        return full_name
    username = (user.get_username() or "").strip()
    if "@" in username:
        return username.split("@")[0]
    return username or "Member"
