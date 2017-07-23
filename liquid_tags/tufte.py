"""
Tufte Tags
----------

This implements a Liquid-style Tufte tag for newthought, sidenote for Pelican.

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

Syntax
------
{% sidenote sidenote-id "Text" %}

Example
-------
{% sidenote for-newsidenote "New sidenote" %}

Output
------
"<label for="for-newsidenote" class="margin-toggle sidenote-number">
</label>
<input type="checkbox" id="for-newsidenote" class="margin-toggle"/>
<span class="sidenote">Text</span>"

"""
import re
from .mdx_liquid_tags import LiquidTags


SIDENOTE_SYNTAX = '''{% sidenote sidenote_id ["content"|'content'] %}'''
SIDENOTE_REGEX = re.compile(
    '''(?P<sidenote_id>[\S+]+)(?:\s+(['"]{0,1})(?P<text>.+)(\\2))?''')
NEWTHOUGHT_SYNTAX = "{% newthought text %}"
# Captures all text within the new thought text.
NEWTHOUGHT_REGEX = re.compile(r'([^"]+)')


@LiquidTags.register('newthought')
def newthought(preprocessor, tag, markup):
    newthought = None

    match = NEWTHOUGHT_REGEX.search(markup)
    if match:
        groups = match.groups()
        newthought = groups[0]

    if newthought:
        newthought_out = """
        <span class="newthought">{}</span>""".format(newthought).strip()
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(NEWTHOUGHT_SYNTAX))

    return newthought_out


@LiquidTags.register('sidenote')
def sidenote(preprocessor, tag, markup):
    match = SIDENOTE_REGEX.search(markup)
    attrs = None
    if match:
        attrs = dict(
            [(key, value.strip())
             for (key, value) in match.groupdict().items() if value])
        sidenote_out = """<label for="{sidenoteid}"
        class="margin-toggle sidenote-number"></label>
        <input type="checkbox" id="{sidenoteid}" class="margin-toggle"/>
        <span class="sidenote">{text}</span>""".format(sidenoteid=attrs['sidenote_id'],text=attrs['text'])
        return sidenote_out
    else:
        raise ValueError('Error processing input. '
                         'Expected syntax: {}'.format(SIDENOTE_SYNTAX))
# ---------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register  # noqa
