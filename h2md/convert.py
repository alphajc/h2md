#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

import re
from bs4 import NavigableString, BeautifulSoup as bs

inline_tags = ['a', 'img', 'b', 'strong', 'em', 'i', 'code', 'del']
# block_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'hr', 'blockquote', 'pre']

block_map = {
    'normal': {
        'h1': '\n# {}\n',
        'h2': '\n## {}\n',
        'h3': '\n### {}\n',
        'h4': '\n#### {}\n',
        'h5': '\n##### {}\n',
        'h6': '\n###### {}\n',
        'hr': '\n\n---\n',
        'div': '{}'
    },
    'intent': {
        'p': '\n{}{}\n',
        'blockquote': '{}> {}',
        'pre': '\n{}```{}\n{}\n{}```\n'
    }
}

inline_map = {
    'normal': {
        'i': '*{}*',
        'em': '*{}*',
        'b': '**{}**',
        'strong': '**{}**',
        'del': '~~{}~~',
        "code": '`{}`'
    },
    'link': {
        'a': '[{}]({})',
        'img': '![{}]({})'
    }
}

def convert(html):
    soup = bs(html, 'html.parser')
    container = soup.select_one('article .post-container') \
        or soup.select_one('article #content') \
        or soup.select_one('article') \
        or soup.select_one('body') \
        or soup
    return __print_tree(container)

def __print_tree(ele, intent = 0, md = ''):
    """递归遍历DOM，为了开发时间暂时就用递归了
    
    Arguments:
        ele {bs} -- 待解析元素
    
    Keyword Arguments:
        intent {int} -- 缩进值 (default: {0})
        md {str} -- 转换后的文档 (default: {''})
    
    Returns:
        str -- 转换后的文档
    """
    if isinstance(ele, NavigableString):
        md = __transform_text(ele, md)
    elif ele.name == 'img':
        md = __transform_img(ele, md)
    elif ele.name == 'a':
        md = __transform_a(ele, md, intent)
    elif ele.name in inline_map['normal'].keys():
        md = __transform_inline_tags(ele, md, intent)
    elif ele.name == 'pre':
        md =  __transform_pre(ele, md, intent)
    elif ele.name in ('ul', 'ol'):
        md = __transform_list_tags(ele, md, intent)
    elif ele.name in block_map['normal'].keys():
        md = __transform_block_normal_tags(ele, md, intent)
    elif ele.name in block_map['intent'].keys():
        md = __transform_block_intent_tags(ele, md, intent)
    elif ele.name == '[document]':
        md = __transform_soup(ele, md, intent)
    else:
        md = __transform_other_tags(ele, md, intent)

    return md
    
def __transform_text(ele, md):
    text = re.compile(r'[\s]+').sub(' ', ele.string)
    text = text if ele.previous_sibling and ele.previous_sibling.name in inline_tags else text.lstrip()
    text = text if ele.next_sibling and ele.next_sibling.name in inline_tags else text.rstrip()
    md += text

    return md

def __transform_img(ele, md):
    md += inline_map['link']['img'].format(ele.get('alt') or '', ele.get('src') or '')

    return md

def __transform_a(ele, md, intent):
    a_inner = ''
    for child in ele.children:
        a_inner = __print_tree(child, intent, a_inner)
    
    if a_inner != '':
        md += inline_map['link']['a'].format(a_inner, ele.get('href') or ele.get_text(strip=True))

    return md

def __transform_pre(ele, md, intent):
    lang_tag = ele.find(class_='hljs')
    if lang_tag: lang_tag['class'].remove('hljs')
    lang = ''.join(lang_tag['class']) if lang_tag else ''
    md += block_map['intent']['pre'].format(' ' * intent, lang, ele.text.strip().replace('\n', '\n' + ' ' * intent), ' ' * intent)
    
    return md

def __transform_inline_tags(ele, md, intent):
    inline_tag_inner = ''
    for child in ele.children:
        inline_tag_inner = __print_tree(child, intent, inline_tag_inner)
    if inline_tag_inner:
        md += inline_map['normal'][ele.name].format(inline_tag_inner)

    return md

def __transform_block_normal_tags(ele, md, intent):
    block_tag_inner = ''
    for child in ele.children:
        block_tag_inner = __print_tree(child, intent, block_tag_inner)
    md += block_map['normal'][ele.name].format(block_tag_inner)

    return md

def __transform_block_intent_tags(ele, md, intent):
    block_tag_inner = ''
    tpl = block_map['intent'][ele.name]
    prev = ' ' * intent

    if ele.parent.name == 'blockquote':
        prev = ele.parent['data-prev']
        ele['data-prev'] = ele.parent['data-prev'] + '> '
        tpl = ele.parent['data-prev'] + '\n' + tpl + '\n'
    elif ele.name == 'blockquote':
        tpl = '\n' + tpl + '\n'
        ele['data-prev'] = ' ' * intent + '> '

    for child in ele.children:
        block_tag_inner = __print_tree(child, intent, block_tag_inner)
    
    tpl = __fill_newline_if_need(ele, tpl)
    md += tpl.format(prev, block_tag_inner)

    return md

def __transform_other_tags(ele, md, intent):
    other_inner = ''
    for child in ele.children:
        other_inner = __print_tree(child, intent, other_inner)
    
    ele.clear()
    ele.append('{}')
    md += ele.decode().format(other_inner)

    return md

def __transform_list_tags(ele, md, intent):
    list_text = '\n'
    if ele.find_parent(re.compile('[ou]l')): intent += 4
    
    line_head = '* ' if ele.name == 'ul' else '{}. '
    for i, e in enumerate(ele.find_all('li', recursive=False)):
        li_inner = ''
        for child in e.children:
            li_inner = __print_tree(child, intent, li_inner)
        list_text += ' ' * intent + line_head.format(i + 1) + li_inner.lstrip() + '\n'
    
    md += __fill_newline_if_need(ele, list_text) if list_text.strip() != '' else ''

    return md

def __transform_soup(ele, md, intent):
    for child in ele.children:
        md = __print_tree(child, intent, md)
        
    return md

def __fill_newline_if_need(ele, text):
    if ele.next_sibling and ele.next_sibling.name in inline_map['normal'].keys() \
        or isinstance(ele.next_sibling, NavigableString) and ele.next_sibling.string.strip() != '':
        text += '\n'

    if ele.previous_sibling and ele.previous_sibling in inline_map['normal'].keys()\
        or isinstance(ele.previous_sibling, NavigableString) and ele.previous_sibling.string.strip() != '':
        text = '\n' + text
    
    return text