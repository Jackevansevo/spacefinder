from django import template

register = template.Library()

busyness_scores = {1: "Busy", 2: "Quite Busy", 3: "Average", 4: "Quite Empty", 5: "Empty"}

def get_busyness_score(value):
    """Converts float 'busyness' rating to human readable value."""
    return busyness_scores.get(round(float(value)))

register.filter('get_busyness_score', get_busyness_score)
