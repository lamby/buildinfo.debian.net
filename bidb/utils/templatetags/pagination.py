from django import template

register = template.Library()

@register.filter
def paginator(querydict, page_number):
    querydict = querydict.copy()
    querydict['page'] = page_number

    if page_number == 1:
        querydict.pop('page')

    return querydict.urlencode()

class PaginationNode(template.Node):
    def __init__(self, page_var, template_file):
        self.page_var = template.Variable(page_var)
        self.template_name = template_file

    def render(self, context):
        # page_var should always be a variable
        page = self.page_var.resolve(context)

        if not getattr(self, 'nodelist_page', False):
            t = template.loader.get_template(self.template_name)
            self.nodelist_page = t.nodelist

        context.push()

        context['page'] = page
        context['_page_url_maker'] = page.paginator.page_linker

        output = self.nodelist_page.render(context)
        context.pop()

        return output
