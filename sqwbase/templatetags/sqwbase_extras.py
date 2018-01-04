from django import template

register = template.Library()

def wrap_heading(text, level):
    h_tag = "h{}".format(2+level)
    return f"<{h_tag}>{text}</{h_tag}>"

register.filter("wrap_heading", wrap_heading)
