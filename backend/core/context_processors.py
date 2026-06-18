def user_display_name(request):
    """Return a friendly user name for templates without showing email domains or @ signs."""
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return {"display_name": ""}

    name = (user.get_full_name() or user.first_name or user.username or "").strip()
    if "@" in name:
        name = name.split("@", 1)[0]
    name = name.replace("@", "").replace("_", " ").strip()
    if not name:
        name = "there"
    return {"display_name": name.title()}
