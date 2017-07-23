"""
Tufte Tag
---------

This implements a Liquid-style Tufte tag for newthought for Pelican.

Uses same schema as https://github.com/clayh53/tufte-jekyll/

Syntax
------
{% newthought Text %}

Example
-------
{% newthought New thought %}

Output
------
<span class="newthought">"New thought"</span>
"""
import re
from .mdx_liquid_tags import LiquidTags

SYNTAX = "{% newthought text %}"
# Captures all text within the new thought text. 
NEWTHOUGHT = re.compile(r'([^"]+)')


@LiquidTags.register('newthought')
def newthought(preprocessor, tag, markup):
    '''Doing the regex parsing and running the create_html function.'''
    newthought = None

    match = NEWTHOUGHT.search(markup)
    if match:
        groups = match.groups()
        newthought = groups[0]

    if newthought:
        newthought_out = """
        <span class="newthought">{}</span>""".format(newthought).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))

    return newthought_out


# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register  # noqa
