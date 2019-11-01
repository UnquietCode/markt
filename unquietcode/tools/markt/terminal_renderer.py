import shutil
import math
import textwrap
import random

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

def underlined(text):
    return f"\x1B[4m{text}\x1B[0m"
    
def bold(text):
    return f"\x1B[1m{text}\x1B[0m"
    
def italics(text):
     return f"\x1B[3m{text}\x1B[0m"

def dim(text):
    return f"\x1b[2m{text}\x1B[0m"

def strikethrough(text):
    return f"\x1B[9m{text}\x1B[0m"


class TerminalRenderer(BaseRenderer):

    def __init__(self):
        super().__init__()
        
        self.render_map['BlockCode'] = self.render_banner
    
    
    def _get_terminal_size(self): # columns, rows tuple
        return shutil.get_terminal_size()
    
    @property
    def _terminal_rows(self):
        return self._get_terminal_size()[1]

    @property
    def _terminal_cols(self):
        return self._get_terminal_size()[0]
    
    @property
    def _spacer(self):
        return "  "
        
    @property
    def _margin(self):
        return math.floor(self._terminal_cols * 0.75)        


    def figlet(self, font, text, space=1, transform=None):
        if transform is not None:
            text = transform(text) 
        
        figlet = Figlet(font=font, width=self._margin)
        lines = figlet.renderText(text).splitlines()
        
        rendered = ""
        space = ' ' * space
        
        for line in lines:
            rendered += f"{space}{line}\n"

        return rendered[0:-1]
    
    
    # generic styles
    
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
    
    # 
    # def render_raw_text(self, token):
        # print(f"it's {token.content}")
        # return self.render_to_plain(token)
        
        
    # inline styles
    
    def render_strong(self, token):
        return bold(self.render_inner(token))


    def render_emphasis(self, token):
        return italics(self.render_inner(token))


    def render_strikethrough(self, token):
        return strikethrough(self.render_inner(token))

        # this doesn't seem to work as well

        # rendered = ''
        # 
        # for c in self.render_inner(token):
        #     rendered += f"{c}\u0336"
        # 
        # return rendered
    
    
    def render_inline_code(self, token):
        return f"\x1B[7m{self.render_inner(token)}\x1B[0m"


    def render_line_break(self, token):
        return '\n'# * len(token.content)


    def render_link(self, token):
        return f"{self.render_inner(token)} ({underlined(token.target)})"

    
    def render_heading(self, token):
        text = self.render_inner(token)
        space = max(2, 3 - token.level)
        
        if token.level == 1:
            return '\n\n' + self.figlet('standard', text.replace(' ', '  '), space=space) + '\n\n'

        elif token.level == 2:
            rendered = self.figlet('ogre', text, space=space)
            
            lines = rendered.splitlines()
            last_line = lines[-1]
            last_line = self._spacer + underlined(last_line[len(self._spacer):])
            lines[-1] = last_line
            rendered = '\n'.join(lines)
            
            return f"\n\n{rendered}\n\n"
        
        elif token.level == 3:
            return '\n\n' + self.figlet('cybermedium', text, space=space) + '\n\n'
            
        elif token.level == 4:
            return f"\n\n{self._spacer}{underlined(bold(self.render_inner(token).upper()))}\n\n"

        elif token.level == 5:
            return f"\n\n{self._spacer}{dim(underlined(bold(self.render_inner(token).upper())))}\n\n"
                    
        elif token.level >= 6:
            return f"\n\n{self._spacer}{dim(underlined(self.render_inner(token).upper()))}\n\n"
        
        else:
            return f"\n\n{self._spacer}{underlined(self.render_inner(token))}\n\n"
        
    
    # def render_banner(self, token):
    #     text = self.render_inner(token)
    #     rendered = ""
    # 
    #     line = "=" * math.ceil((len(text) * 1.35))
    #     padding = math.ceil((len(line) - len(text)) / 2)
    #     inner_line = f"{padding * ' '}{text}{padding * ' '}"
    #     return f"{line}\n\n{inner_line}\n{line}\n"
    # # 
    #     # rendered += '\n\n' + text + '\n' + rendered
        # return rendered

    def render_banner(self, token):
        
        def invert(text):
            new = []
            
            for x in text:
                if x.isupper():
                    new.append(x.lower())
                elif x.islower():
                    new.append(x.upper())
                else:
                    new.append(x)
            
            return ''.join(new)
        
        text = self.render_inner(token)
        text = self.figlet('com_sen_', invert(text), space=2)
        
        lines = text.splitlines()
        line = "=" * (max(len(lines[0]), len(lines[-1])) -1)
        
        return f"{line}\n\n{text}\n{line}\n"
    
        
    
    def render_thematic_break(self, token):
        width = math.floor(self._terminal_cols * 0.45)
        
        rendered = f"{self._spacer}◈"
        rendered += "─" * width
        rendered += "◈\n\n"
        return rendered
        
    
    def render_paragraph(self, token):
        text = self.render_inner(token)
        rendered = ""
        
        text = " ".join(text.splitlines())
        lines = textwrap.wrap(text.strip(), width=self._margin)
        
        for line in lines:
            rendered += f"{self._spacer}{line}\n"
        
        if rendered.strip():
            rendered += "\n"
        
        return rendered
        

    def render_quote(self, token):
        innards = self.render_inner(token)
        rendered = ''

        for line in innards.splitlines():
            if line.strip():
                rendered += f"{self._spacer}\x1B[37m|  {line.strip()}\x1B[0m\n"
            else:
                rendered += line

        rendered += "\n"
        return rendered
    
    
    def render_list(self, token):
        rendered = ""
        counter = None
        
        if token.start is not None:
            counter = token.start
        
        for child in token.children:
            if counter is not None:
                rendered += f"{self._spacer}{counter}. "
                counter += 1
            else:
                prefix = ' ' * ((child.prepend - 2) * 2)
                rendered += f"{self._spacer}{prefix}{child.leader} "
            
            rendered += self.render(child)
        
        rendered += "\n"
        return rendered
    
    
    def render_list_item(self, token):
        rendered = ""
        line = self.render_inner(token)
        
        if line.strip():
            rendered += f"{line.strip()}\n"
        
        return rendered
        
    
    def render_block_code(self, token):
        innards = self.render_inner(token)
        rendered = '\n'

        for line in innards.splitlines():
            if line.strip():
                wrapped_lines = textwrap.wrap(line.strip(), width=self._margin)
                
                for wrapped_line in wrapped_lines:
                    rendered += f"  \x1B[37m|  {wrapped_line}\x1B[0m\n"
            else:
                rendered += f"  \x1B[37m|  {line}\x1B[0m\n"

        rendered += "\n"
        return rendered