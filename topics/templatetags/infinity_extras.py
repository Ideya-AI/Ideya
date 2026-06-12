import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, q):
    """Wrap case-insensitive matches of `q` within `text` in <mark>."""
    text = str(text)
    if not q:
        return text
    try:
        pattern = re.compile("(" + re.escape(str(q)) + ")", re.IGNORECASE)
    except re.error:
        return text
    parts = pattern.split(text)
    out = "".join(
        f"<mark>{escape(p)}</mark>" if i % 2 else escape(p) for i, p in enumerate(parts)
    )
    return mark_safe(out)


@register.filter
def lead_hl(text, phrase):
    """Wrap the first occurrence of `phrase` within `text` in <span class="hl">."""
    text = str(text)
    if not phrase:
        return escape(text)
    idx = text.lower().find(str(phrase).lower())
    if idx < 0:
        return escape(text)
    before, mid, after = (
        text[:idx],
        text[idx : idx + len(phrase)],
        text[idx + len(phrase) :],
    )
    return mark_safe(
        f'{escape(before)}<span class="hl">{escape(mid)}</span>{escape(after)}'
    )
