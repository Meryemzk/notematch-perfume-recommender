from collections import Counter
from decimal import Decimal

from perfumes.models import Perfume
from .models import Mood, UserPreferenceProfile

COMMON_NOTE_TAGS = [
    "citrus", "fresh", "lavender", "vanilla", "rose", "floral", "musk",
    "woody", "cedar", "sandalwood", "amber", "spicy", "pepper", "bergamot",
    "jasmine", "iris", "oud", "patchouli", "tonka", "leather", "aquatic",
    "apple", "pear", "orange", "lemon", "grapefruit", "tea", "mint", "coconut"
]


def budget_bounds(budget_range):
    bounds = {
        "under_30": (Decimal("0"), Decimal("30")),
        "30_60": (Decimal("30"), Decimal("60")),
        "60_100": (Decimal("60"), Decimal("100")),
        "over_100": (Decimal("100"), None),
    }
    return bounds.get(budget_range, (None, None))


def extract_tags_from_favourites(favourite_names):
    """Use perfumes already in the catalogue to understand the user's taste."""
    tags = []
    for name in favourite_names:
        name = (name or "").strip()
        if not name:
            continue
        matches = Perfume.objects.filter(name__icontains=name)[:5]
        for perfume in matches:
            notes_text = (perfume.notes or "").lower()
            for tag in COMMON_NOTE_TAGS:
                if tag in notes_text:
                    tags.append(tag)
    return tags


def get_or_create_profile_from_post(user, post_data):
    """Create/update a saved preference profile only when the user chooses.

    First survey completion creates a profile. Existing profile is kept unless
    update_saved_profile is checked or the profile page is used.
    """
    values = {
        "favourite_perfume_1": (post_data.get("favourite_perfume_1") or "").strip(),
        "favourite_perfume_2": (post_data.get("favourite_perfume_2") or "").strip(),
        "favourite_perfume_3": (post_data.get("favourite_perfume_3") or "").strip(),
        "preferred_gender": post_data.get("preferred_gender") or "no_preference",
        "style_preference": post_data.get("style_preference") or "both",
        "budget_range": post_data.get("budget_range") or "no_preference",
    }

    valid_gender = [choice[0] for choice in UserPreferenceProfile.GENDER_PREFERENCE_CHOICES]
    valid_style = [choice[0] for choice in UserPreferenceProfile.STYLE_PREFERENCE_CHOICES]
    valid_budget = [choice[0] for choice in UserPreferenceProfile.BUDGET_CHOICES]

    if not all([values["favourite_perfume_1"], values["favourite_perfume_2"], values["favourite_perfume_3"]]):
        return None, "Please enter three favourite perfumes so the system can learn your past preferences."
    if values["preferred_gender"] not in valid_gender or values["style_preference"] not in valid_style or values["budget_range"] not in valid_budget:
        return None, "Invalid preference selection. Please try again."

    profile = UserPreferenceProfile.objects.filter(user=user).first()
    should_update = post_data.get("update_saved_profile") == "yes"

    if profile is None:
        profile = UserPreferenceProfile.objects.create(user=user, **values)
    elif should_update:
        for key, value in values.items():
            setattr(profile, key, value)
        profile.save()

    return profile, None


def create_mood_result(submission, questions, post_data, profile):
    total_energic = 0
    total_relax = 0
    tags = []

    for question in questions:
        picked_option_id = post_data.get(f"q_{question.id}")
        if not picked_option_id:
            return "Please answer all mood and scent questions."

        option = question.options.filter(id=picked_option_id).first()
        if not option:
            return "Invalid selection. Please try again."

        from .models import SurveyAnswer
        SurveyAnswer.objects.create(submission=submission, question=question, option=option)

        total_energic += option.energic_points
        total_relax += option.relax_points
        if option.note_tag:
            tags.append(option.note_tag.strip().lower())

    tags.extend(extract_tags_from_favourites(profile.favourite_names))
    mood_name = "Energic" if total_energic >= total_relax else "Relaxation"
    mood, _ = Mood.objects.get_or_create(name=mood_name)
    top_tags = [tag for tag, _count in Counter(tags).most_common(7)]

    submission.total_energic = total_energic
    submission.total_relax = total_relax
    submission.result_mood = mood
    submission.top_note_tags = ",".join(top_tags)
    submission.save()
    return None


def rank_perfumes_for_submission(submission):
    perfumes = Perfume.objects.filter(moods=submission.result_mood, is_active=True).distinct()
    tags = [tag.strip().lower() for tag in (submission.top_note_tags or "").split(",") if tag.strip()]
    favourite_names = submission.favourite_names
    min_price, max_price = budget_bounds(submission.budget_range)

    ranked = []
    for perfume in perfumes:
        score = 0
        reasons = []
        notes_text = (perfume.notes or "").lower()

        score += 5
        reasons.append(f"matches your {submission.result_mood.name} mood")

        matched_tags = []
        for tag in tags:
            if tag in notes_text and tag not in matched_tags:
                score += 3
                matched_tags.append(tag)
        if matched_tags:
            reasons.append("shares notes you like: " + ", ".join(matched_tags))

        if submission.preferred_gender == "no_preference":
            score += 1
        elif perfume.gender_category in [submission.preferred_gender, "unisex"]:
            score += 3
            reasons.append("fits your gender preference")
        else:
            score -= 4

        if submission.style_preference == "both":
            score += 1
        elif perfume.style_category == submission.style_preference:
            score += 3
            reasons.append(f"fits your {submission.get_style_preference_display().lower()} style choice")
        else:
            score -= 2

        if submission.budget_range == "no_preference":
            score += 1
        else:
            price = perfume.price or Decimal("0")
            in_budget = True
            if min_price is not None and price < min_price:
                in_budget = False
            if max_price is not None and price > max_price:
                in_budget = False
            if in_budget:
                score += 3
                reasons.append("fits your budget")
            else:
                score -= 3

        if perfume.name.lower() in [name.lower().strip() for name in favourite_names if name]:
            score -= 5
            reasons.append("you already listed this as a favourite, so alternatives are prioritised")

        ranked.append({
            "perfume": perfume,
            "score": score,
            "matched_tags": matched_tags,
            "reasons": reasons[:5],
        })

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked, tags
