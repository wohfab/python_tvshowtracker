# import database
# import sqlite3
# import lxml

from html_IO import *
import wikipydia
import tvshowlist
import re
from bs4 import BeautifulSoup

# tvShow = "Vikings"
tvShow = "Sherlock"
# tvShow = "Simpsons"

tableStart = '<table class="wikitable plainrowheaders" style="width'
tableEnd = '</table>'

tableRowStart = '<tr'
tableRowEnd = '</tr>'

tableDateStart = '<td'
tableDateEnd = '</td>'

wikiLinkPrefix = '<a href="http://en.wikipedia.org/'


def crawl(tv_show):
    tv_show_link = tvshowlist.get_tv_show_link(tv_show)
    tv_show_code = tvshowlist.get_tv_show_code(tv_show)
    print('You successfully crawled: ', tv_show_link, tv_show_code)
    tv_show_content = wikipydia.query_text_rendered(tv_show_code[1])["html"].encode('ascii', 'ignore')
    write_html("files/output.html", tv_show_content)


def write_html(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()


def read_html(file_name):
    f = open(file_name, "r")
    content = f.read()
    f.close()
    return content


def fix_a_href(file_name):
    content = read_html(file_name)
    fixed_a_href = re.sub(r'<a href="/', wikiLinkPrefix, content)
    write_html("files/fixed_a_href.html", fixed_a_href)


def remove_a_href(file_name):
    content = read_html(file_name)
    removed_a_href = re.compile(r'<a href.*>')
    write_html("files/removed_a_href.html", removed_a_href.sub('', content))


def get_number_of_tables(file_name):
    number_of_tables = len(re.findall(tableStart, read_html(file_name)))
    return number_of_tables


def get_number_of_table_rows(table):
    number_of_table_rows = len(re.findall(tableRowStart, table))
    return number_of_table_rows


def get_tables(file_name):
    tables = []
    content = read_html(file_name)
    for number in range(get_number_of_tables(file_name)):
        tables.append(tableStart + content.split(tableStart)[number + 1].split(tableEnd)[0] + tableEnd)
    tables_as_html = ''.join(tables)
    write_html("files/tables.html", tables_as_html)
    return tables


def get_table_rows(table):
    table_rows = []
    for number in range(get_number_of_table_rows(table)):
        table_rows.append(tableRowStart + table.split(tableRowStart)[number + 1].split(tableRowEnd)[0] + tableRowEnd)
    return table_rows


def get_episodes(table):
    episodes = re.findall("vevent", table)
    return episodes


def get_table_row_data(table):
    episodes = get_episodes(table)
    table_row_data = re.compile(r'<td.*>')
    write_html("files/strip.html", table_row_data.sub('', ''.join(episodes)))


def test():
    crawl(tvShow)
    get_tables('files/output.html')
    fix_a_href('files/tables.html')

test()
