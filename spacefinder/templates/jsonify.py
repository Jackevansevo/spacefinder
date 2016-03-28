from django.template import Library
import json

register = Library()


@register.filter(name="jsonify")
def jsonify(value):
    return json.dumps(str(value))
