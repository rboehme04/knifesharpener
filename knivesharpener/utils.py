from io import BytesIO
from django import template
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa 

import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def render_to_pdf(template_src, context_dict, id):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('cp1252')), result)
    filename = f"knivesharpener/pdf/{id}.pdf"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(result.getvalue()))
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"pdf/{title}.pdf"
    heading = f"# {title} <br\>"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def delete_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"pdf/{title}.pdf"
    default_storage.delete(filename)
    
