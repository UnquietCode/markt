import mistletoe

from . import TerminalRenderer


def render_markdown(text):
    rendered = mistletoe.markdown(text, TerminalRenderer)
    return rendered