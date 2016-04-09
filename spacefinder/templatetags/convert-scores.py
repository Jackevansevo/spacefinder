from django import template

register = template.Library()

busyness_scores = {
    1: "Busy", 2: "Quite Busy", 3: "Average", 4: "Quite Empty", 5: "Empty"
}


@register.filter(name='get_busyness_score')
def get_busyness_score(value):
    """Converts float 'busyness' rating to human readable value."""
    return busyness_scores.get(round(float(value)))


@register.filter(name='rating_streak_as_days')
def rating_streak_as_days(value):
    """Converts an integer value to a string followed by day/days"""
    return "1 day" if value == 1 else str(value) + "days"
