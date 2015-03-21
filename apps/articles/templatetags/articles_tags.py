# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import smart_str
from django.template import TemplateSyntaxError
try:
    # Pre django 1.2
    from django.utils.itercompat import groupby
except ImportError:
    from itertools import groupby
# from miles.shortcuts import render_to_string
from django.template.loader import render_to_string
from django.template import RequestContext
from django.db.models import Q

from .util import get_block_template
from .models import Article


class GetArticleNode(template.Node):
    def __init__(self, blocks, args, kwargs, asvar):
        self.blocks = [template.Variable(b) for b in blocks]
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def __repr__(self):
        return '<GetArticleNode>'

    def render(self, context):
        blocks = [b.resolve(context) for b in self.blocks]
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])

        request = context.get('request', None)

        articles = self.get_articles(blocks, request=request, *args, **kwargs)

        if self.asvar:
            context[self.asvar] = articles
            return ''
        else:
            template_name = get_block_template(blocks[0])
            context = {'articles': articles, 'block': blocks[0]}
            return render_to_string(template_name, context, RequestContext(request))

    def get_articles(self, blocks, limit=None, order=None, request=None):
        multiblock = len(blocks) > 1
        articles = Article.live_objects.all()

        if multiblock:
            aux = []
            for b in blocks:
                aux.append(Q(block__exact=b))
            articles = articles.filter(*aux)
        else:
            articles = articles.filter(block__icontains=blocks[0])

        # Order
        if order is not None:
            if order == 'random':
                articles = articles.order_by('?')

        # Multigroup groups and Limit
        if multiblock:
            tmp = {}
            for block, l in groupby(articles, lambda h: h.block):
                tmp[block] = list(l)[:limit]
            articles = tmp
        else:
            articles = articles[:limit]

        return articles


def get_articles(parser, token):
    """
    Returns articles for a given block, optional filtred by extra arguments.

    If a context var is given the articles are added to the context, if not
    they will be redered using the default template for the block (defined in
    ARTICLE_BLOCKS 'template_name' setting). In case no context var is given
    and no default template is defined for the block an exception will we
    raised.

    if more than one block is given (comma separated) you must add the as var
    arguments, the articles for each block will be grouped using django's
    groupby.

    Usage:
      {% get_articles block[,block2,block3] [arg1,arg2,kwargn1=kwargv1,...] [as var] %}

    """
    bits = token.split_contents()
    if len(bits) < 2:
        msg = '"%s" takes at least one argument (block(s) name(s)).' % bits[0]
        raise TemplateSyntaxError(msg)
    blocks = bits[1].split(',')

    args = []
    kwargs = {}
    asvar = None

    if len(bits) > 2:
        bits = iter(bits[2:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))

    #if len(blocks) != 1 and asvar is not None:
    #    msg = ('"%s" You must include as var parameters when '
    #           'passing more than one block.' % bits[0])
    #    raise TemplateSyntaxError(msg)

    return GetArticleNode(blocks, args, kwargs, asvar)


register = template.Library()
register.tag(get_articles)
