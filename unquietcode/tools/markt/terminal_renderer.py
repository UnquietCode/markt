import shutil
import math
import textwrap

from mistletoe.base_renderer import BaseRenderer
from pyfiglet import Figlet

# https://github.com/miyuchina/mistletoe/blob/master/mistletoe/base_renderer.py
# 
    # 'Document':       self.render_document,
    # 'Strong':         self.render_strong,
    # 'Emphasis':       self.render_emphasis,
    # 'Strikethrough':  self.render_strikethrough,
    # 'LineBreak':      self.render_line_break,
    # 'Quote':          self.render_quote,
    # 'Paragraph':      self.render_paragraph,
    # 'ThematicBreak':  self.render_thematic_break,
    # 'InlineCode':     self.render_inline_code,
    # 'BlockCode':      self.render_block_code,

    # 'List':           self.render_list,
    # 'ListItem':       self.render_list_item,
    # 'Heading':        self.render_heading,
    # 'SetextHeading':  self.render_heading,
    # 'Link':           self.render_link,
    # 'RawText':        self.render_raw_text,
    
    # 'AutoLink':       self.render_auto_link,
    # 'EscapeSequence': self.render_escape_sequence,
    # 'Image':          self.render_image,
    
    # 'CodeFence':      self.render_block_code,
    
    # 'Table':          self.render_table,
    # 'TableRow':       self.render_table_row,
    # 'TableCell':      self.render_table_cell,
    

# TODO wrapping by width of terminal

class TerminalRenderer(BaseRenderer):
    """
    """

    def __init__(self, *extras):
        super().__init__(*extras)
    
    def _get_terminal_size(self): # columns, rows tuple
        return shutil.get_terminal_size()
    
    @property
    def _terminal_rows(self):
        return self._get_terminal_size()[1]

    @property
    def _terminal_cols(self):
        return self._get_terminal_size()[0]
    
    def render_document(self, token):
        rendered = "\n"
        rendered += self.render_inner(token)
        return rendered

    def render_to_plain(self, token):
        if hasattr(token, 'children'):
            inner = [self.render_to_plain(child) for child in token.children]
            return ''.join(inner)
        else:
            return token.content


    def render_strong(self, token):
        return f"\x1B[1m{self.render_inner(token)}\x1B[0m"


    def render_emphasis(self, token):
        return f"\x1B[3m{self.render_inner(token)}\x1B[0m"


    def render_strikethrough(self, token):

        # this doesn't seem to work as well
        return f"\x1B[9m{self.render_inner(token)}\x1B[0m"

        # rendered = ''
        # 
        # for c in self.render_inner(token):
        #     rendered += f"{c}\u0336"
        # 
        # return rendered
    
    
    def render_inline_code(self, token):
        return f"\x1B[47m\x1B[30m{self.render_inner(token)}\x1B[0m"


    def render_line_break(self, token):
        return '\n'# * len(token.content)


    def render_link(self, token):
        # return f"\x1B]8;;http://www.google.com\x07link\x1B]8;;\x07"
        # return "http://www.google.com"
        # return "\x1B[59m  http://foo.bar\x1B[0m"
        return "http://foo.bar"
    # 
    # def render_raw_text(self, token):
        # print(f"it's {token.content}")
        # return self.render_to_plain(token)

    # HEADING_TO_FONTS = {
    #     0: 'term',
    #     1: 'small',
    #     2: 'small',
    #     3: 'small',
    #     4: 'small',
    #     5: 'term',
    #     6: 'term', # TODO can we do better?
    # 
    #     # ogre
    #     # rectangles
    # }
    
    def render_paragraph(self, token):
        return f"{self.render_inner(token)}\n\n"


    def render_heading(self, token):
        # figlet = Figlet()
        # figlet.setFont(font=self.HEADING_TO_FONTS[token.level])
        # return '\n'+figlet.renderText(self.render_inner(token))
        return f"  {'#' * token.level} {self.render_inner(token)}\n"


    def render_quote(self, token):
        innards = self.render_inner(token)
        rendered = ''

        for line in innards.splitlines():
            if line.strip():
                rendered += f"  \x1B[37m|  {line}\x1B[0m\n"
            # else:
                # rendered += "\n"

        rendered += "\n"
        return rendered
    
    
    def render_list(self, token):
        rendered = ""
        counter = None
        
        if token.start is not None:
            counter = token.start
        
        for child in token.children:
            if counter is not None:
                rendered += f"{counter}. "
                counter += 1
            else:
                prefix = ' ' * ((child.prepend - 2) * 2)
                rendered += f"{prefix}{child.leader} "
            
            rendered += self.render(child)
        
        rendered += "\n"
        return rendered
    
    
    def render_list_item(self, token):
        rendered = ""
        line = self.render_inner(token)
        
        if line.strip():
            rendered += f"{line.strip()}\n"
        
        return rendered
        
    
    def render_thematic_break(self, token):
        width = math.floor(self._terminal_cols * 0.55)
        
        rendered = "◈"
        rendered += "─" * width
        rendered += "◈\n\n"
        return rendered
        
    
    def render_block_code(self, token):
        width = math.floor(self._terminal_cols * 0.9)
        innards = self.render_inner(token)
        rendered = '\n'

        for line in innards.splitlines():
            if line.strip():
                wrapped_lines = textwrap.wrap(line.strip(), width=width)
                
                for wrapped_line in wrapped_lines:
                    rendered += f"  \x1B[37m|  {wrapped_line}\x1B[0m\n"
            else:
                rendered += f"  \x1B[37m|  {line}\x1B[0m\n"

        rendered += "\n"
        return rendered