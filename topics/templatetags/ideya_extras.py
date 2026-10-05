import os
import re

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static as static_url
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def static_v(path):
    """Like {% static %}, but in DEBUG appends a ?v=<mtime> cache-buster so an
    edited CSS/JS file is refetched on the next reload instead of being served
    stale from the browser cache. No-op in production — those assets are already
    content-hashed by ManifestStaticFilesStorage, so the URL is left untouched."""
    url = static_url(path)
    if settings.DEBUG:
        abs_path = finders.find(path)
        if abs_path and os.path.exists(abs_path):
            stamp = int(os.path.getmtime(abs_path))
            url = f"{url}{'&' if '?' in url else '?'}v={stamp}"
    return url


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


@register.filter
def dictget(mapping, key):
    """Look up a dict by a (possibly non-string) key — templates can't do d[var]."""
    if isinstance(mapping, dict):
        return mapping.get(str(key), "")
    return ""


@register.filter
def amp_nbsp(text):
    """Bind "&" to the word after it, so a wrapping title never strands it
    alone on a line ("Loneliness / & / Community"), and make hyphens
    non-breaking so "Phase-Out" never splits into "Phase-" / "Out"."""
    return re.sub(r"(?<=\w)-(?=\w)", "\u2011", str(text).replace(" & ", " &\u00a0"))


@register.filter
def num(text):
    """A displayed number: a hyphen used as a minus becomes a true minus,
    then caret exponents become superscripts (sup_exp)."""
    from topics.models import minus_sign

    return sup_exp(minus_sign(text))


@register.filter
def sup_exp(text):
    """Render caret exponents as real superscripts: 10^26 -> 10<sup>26</sup>.

    Compute thresholds are written in the source JSON as ASCII (`10^26`) so the
    content stays plain text and greppable; typing `10²⁶` into the data would
    break that register and can't be searched. The transform belongs here, at
    the display edge — a reader should not have to parse a caret.
    """
    s = str(text)
    if "^" not in s:
        return escape(s)
    out, last = [], 0
    for m in re.finditer(r"\^(-?\d+)", s):
        out.append(escape(s[last : m.start()]))
        out.append(f"<sup>{escape(m.group(1))}</sup>")
        last = m.end()
    out.append(escape(s[last:]))
    return mark_safe("".join(out))
