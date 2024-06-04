import requests
from bs4 import BeautifulSoup
import lxml


response = requests.get("https://www.etsy.com/help/categories/seller#node-id-1")

print(response.status_code)

soup = BeautifulSoup(response.text, "lxml").body

ul_category_list = soup.select_one("ul.category-list")


def etsy_indexer(
    soup,
    css_selector,
    css_selector_inc,
    i,
    index_list,
    file_name="output.txt",
    file=None,
):

    if not file:
        with open(file_name, "w") as file:
            file.write("")

    indexed_txt = ""
    new_i = i + 1
    selector = css_selector + (new_i * css_selector_inc)

    if not soup:
        return indexed_txt

    for s in soup:
        if i >= len(index_list):
            index_list.append(0)
        index_list[i] += 1
        id = ".".join([str(ind) for ind in index_list])
        cat = s.span.text
        indexed_el = f"{id}. {cat}"
        print(indexed_el)
        with open(file_name, "a") as file:
            file.write(indexed_el + "\n")

        new_soup = s.select(selector)
        etsy_indexer(
            new_soup, css_selector, css_selector_inc, new_i, index_list, file=file
        )

    if index_list:
        del index_list[-1]


index_list = []
i = 0

class_ = "category-list"
css_selector = f"ul.{class_} > li "
css_selector_inc = "> ul > li "

lis = ul_category_list.select(css_selector)

etsy_indexer(lis, css_selector, css_selector_inc, i, index_list)
