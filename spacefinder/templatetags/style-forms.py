from django.template import Library

register = Library()


@register.filter(name='placeholder')
def placeholder(value, token):
    value.field.widget.attrs["placeholder"] = token
    return value


@register.filter(name="addClass")
def addClass(value, newClass):
    value.field.widget.attrs["class"] = newClass
    return value


@register.filter(name="addID")
def addID(value, newID):
    value.field.widget.attrs["id"] = newID
    return value
