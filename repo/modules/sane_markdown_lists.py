"""
Modify the behavior of Lists in Python-Markdown to act in a sane manner.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as etree
from typing import TYPE_CHECKING

from markdown import Extension
from markdown.blockparser import BlockParser
from markdown.blockprocessors import (
    ListIndentProcessor,
    OListProcessor,
    ParagraphProcessor
)

if TYPE_CHECKING:                    
    from markdown import blockparser

MIN_NESTED_LIST_INDENT = 2
assert MIN_NESTED_LIST_INDENT > 1, "'MIN_NESTED_LIST_INDENT' must be > 1"

class SaneListIndentProcessor(ListIndentProcessor):
    """ Process children of list items.

    Example

        * a list item
            process this part

            or this part

    """

    def __init__(self, *args):
        super().__init__(*args)
        self.INDENT_RE = re.compile(r'^(([ ])+)')

    def test(self, parent: etree.Element, block: str) -> bool:
        return block.startswith(' ' * MIN_NESTED_LIST_INDENT) and\
            not self.parser.state.isstate('detabbed') and\
            (parent.tag in self.ITEM_TYPES or (len(parent) and parent[-1] is not None and (parent[-1].tag in
                                                                                           self.LIST_TYPES)))

    def get_level(self, parent: etree.Element, block: str) -> tuple[int, etree.Element]:
        """ Get level of indentation based on list level. """
                          
        m = self.INDENT_RE.match(block)
        if m:
            indent_level = len(m.group(1)) / MIN_NESTED_LIST_INDENT
        else:
            indent_level = 0
        if self.parser.state.isstate('list'):
                                                                          
            level = 1
        else:
                                                                
            level = 0
                                                                      
        while indent_level > level:
            child = self.lastChild(parent)
            if child is not None and (child.tag in self.LIST_TYPES or child.tag in self.ITEM_TYPES):
                if child.tag in self.LIST_TYPES:
                    level += 1
                parent = child
            else:
                                                                         
                break
        return level, parent

    def detab(self, text: str, length: int | None = None) -> tuple[str, str]:
        """ Remove a tab from the front of each line of the given text. """
        if length is None:
            length = MIN_NESTED_LIST_INDENT
        newtext = []
        lines = text.split('\n')
        for line in lines:
            if line.startswith(' ' * length):
                newtext.append(line[length:])
            elif not line.strip():
                newtext.append('')
            else:
                break
        return '\n'.join(newtext), '\n'.join(lines[len(newtext):])

    def looseDetab(self, text: str, level: int = 1) -> str:
        """ Remove indentation from front of lines but allowing dedented lines. """
        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith(' ' * MIN_NESTED_LIST_INDENT * level):
                lines[i] = lines[i][MIN_NESTED_LIST_INDENT * level:]
        return '\n'.join(lines)

class SaneOListProcessor(OListProcessor):
    """ Override `SIBLING_TAGS` to not include `ul` and set `LAZY_OL` to `False`. """

    SIBLING_TAGS = ['ol']
    """ Exclude `ul` from list of siblings. """
    LAZY_OL = False
    """ Disable lazy list behavior. """

    def __init__(self, parser: blockparser.BlockParser):
        super().__init__(parser)
        max_list_start_indent = self.tab_length
                                          
        self.RE = re.compile(r'^[ ]{0,%d}[\*_]{0,2}\d+\.[ ]+(.*)' % max_list_start_indent)
                                                                           
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}([\*_]{0,2})((\d+\.))[ ]+(.*)' % (MIN_NESTED_LIST_INDENT - 1))
                                                       
        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}[\*_]{0,2}((\d+\.)|[*+-])[ ]+.*' %
                                    (MIN_NESTED_LIST_INDENT, self.tab_length * 2))

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
                                                
        items = self.get_items(blocks.pop(0))
        sibling = self.lastChild(parent)

        if sibling is not None and sibling.tag in self.SIBLING_TAGS:
                                                                   
            lst = sibling
                                                                         
            if lst[-1].text:
                                                                       
                p = etree.Element('p')
                p.text = lst[-1].text
                lst[-1].text = ''
                lst[-1].insert(0, p)
                                                                                 
            lch = self.lastChild(lst[-1])
            if lch is not None and lch.tail:
                p = etree.SubElement(lst[-1], 'p')
                p.text = lch.tail.lstrip()
                lch.tail = ''

            li = etree.SubElement(lst, 'li')
            self.parser.state.set('looselist')
            firstitem = items.pop(0)
            self.parser.parseBlocks(li, [firstitem])
            self.parser.state.reset()
        elif parent.tag in ['ol', 'ul']:
                                                                            
            lst = parent
        else:
                                                                       
            lst = etree.SubElement(parent, self.TAG)
                                                    
            if not self.LAZY_OL and self.STARTSWITH != '1':
                lst.attrib['start'] = self.STARTSWITH

        self.parser.state.set('list')
                                                                        
        for item in items:
            if item.startswith(" " * MIN_NESTED_LIST_INDENT):
                                                                  
                self.parser.parseBlocks(lst[-1], [item])
            else:
                                                                   
                li = etree.SubElement(lst, 'li')
                self.parser.parseBlocks(li, [item])
        self.parser.state.reset()

    def looseDetab(self, text: str, indent_length: int, level: int = 1) -> str:
        """ Remove indentation from front of lines but allowing dedented lines. """
        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith(' ' * indent_length * level):
                lines[i] = lines[i][indent_length * level:]
        return '\n'.join(lines)

    def get_items(self, block: str) -> list[str]:
        """ Break a block into list items. """
                                                                     
        if (indent_len := len(block) - len(block.lstrip())) > 0:
            block = self.looseDetab(block, indent_len)
        items = []
        for line in block.split('\n'):
            m = self.CHILD_RE.match(line)
            if m:
                                         
                if not items:
                                                                 
                    INTEGER_RE = re.compile(r'(\d+)')
                    self.STARTSWITH = INTEGER_RE.match(m.group(2)).group()
                                    
                items.append(m.group(1) + m.group(4))
            elif self.INDENT_RE.match(line):
                                                             
                if items[-1].startswith(' ' * MIN_NESTED_LIST_INDENT):
                                                                      
                    items[-1] = '{}\n{}'.format(items[-1], line)
                else:
                    items.append(line)
            else:
                                                                             
                items[-1] = '{}\n{}'.format(items[-1], line)
        return items

class SaneUListProcessor(SaneOListProcessor):
    """ Override `SIBLING_TAGS` to not include `ol`. """

    TAG: str = 'ul'
    SIBLING_TAGS = ['ul']
    """ Exclude `ol` from list of siblings. """

    def __init__(self, parser: blockparser.BlockParser):
        super().__init__(parser)
                                                                  
        max_list_start_indent = self.tab_length
        self.RE = re.compile(r'^[ ]{0,%d}[*+-][ ]+(.*)' % max_list_start_indent)
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([*+-]))[ ]+(.*)' % (MIN_NESTED_LIST_INDENT - 1))

    def get_items(self, block: str) -> list[str]:
        """ Break a block into list items. """
                                                                     
        if (indent_len := len(block) - len(block.lstrip())) > 0:
            block = self.looseDetab(block, indent_len)
        items = []
        for line in block.split('\n'):
            m = self.CHILD_RE.match(line)
            if m:
                                    
                items.append(m.group(3))
            elif self.INDENT_RE.match(line):
                                                             
                if items[-1].startswith(' ' * MIN_NESTED_LIST_INDENT):
                                                                      
                    items[-1] = '{}\n{}'.format(items[-1], line)
                else:
                    items.append(line)
            else:
                                                                             
                items[-1] = '{}\n{}'.format(items[-1], line)
        return items

class SaneParagraphProcessor(ParagraphProcessor):
    """ Process Paragraph blocks. """

    def __init__(self, parser: BlockParser):
        super().__init__(parser)
        max_list_start_indent = self.tab_length
        self.LIST_RE = re.compile(r"\s{2}\n(\s{0,%d}[\d+*-])" % max_list_start_indent)

    def run(self, parent: etree.Element, blocks: list[str]) -> None:
        block = blocks.pop(0)
        if block.strip():
                                                                        
            if self.parser.state.isstate('list'):
                                             
                sibling = self.lastChild(parent)
                if sibling is not None:
                                           
                    if sibling.tail:
                        sibling.tail = '{}\n{}'.format(sibling.tail, block)
                    else:
                        sibling.tail = '\n%s' % block
                else:
                                           
                    if parent.text:
                        parent.text = '{}\n{}'.format(parent.text, block)
                    else:
                        parent.text = block.lstrip()
            else:
                                                    
                next_list_block = None
                if list_match := self.LIST_RE.search(block):
                    list_start = list_match.end() - len(list_match.group(1))
                    next_list_block = block[list_start:]
                    block = block[:list_start]

                p = etree.SubElement(parent, 'p')
                p.text = block.lstrip()

                if next_list_block:
                    self.parser.parseBlocks(p, [next_list_block])

class SaneListExtension(Extension):
    """ Add sane lists to Markdown. """

    def extendMarkdown(self, md):
        """ Override existing Processors. """
        md.parser.blockprocessors.register(SaneListIndentProcessor(md.parser), 'indent', 90)
        md.parser.blockprocessors.register(SaneOListProcessor(md.parser), 'olist', 40)
        md.parser.blockprocessors.register(SaneUListProcessor(md.parser), 'ulist', 30)
        md.parser.blockprocessors.register(SaneParagraphProcessor(md.parser), 'paragraph', 10)

        md.parser.blockprocessors.deregister('code')

def makeExtension(**kwargs):                    
    return SaneListExtension(**kwargs)
