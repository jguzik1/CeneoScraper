import requests
from bs4 import BeautifulSoup

def get_element(ancestor, selector = None, attribute = None, return_list = False):
    try:
        if return_list:
            return [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except AttributeError:
        return None

# product_code = input("Podaj kod produktu: ")
product_code = "95319759"
# url = "https://www.ceneo.pl/" + product_code + "#tab=reviews"
# url = "https://www.ceneo.pl/{}#tab=reviews".format(product_code)
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
page_dom = BeautifulSoup(response.text, "html.parser")
opinions = page_dom.select("div.js_product-review")
all_opinions = []
for opinion in opinions:
    single_opinion ={
        "opinion" : opinion["data-entry-id"],
        "author" : get_element(opinion,"span.user-post__author-name"),
        "recommendaton" : get_element(opinion,"span.user-post__author-recomendation > em"),
        "stars" : opinion.select_one("span.user-post__score-count").text.strip(),
        "purchased" : get_element(opinion,"div.review-pz"),
        "opinion_date" : get_element(opinion,"span.user-post__published > time:nth-child(1)", "datetime"),
        "purchase_date" : get_element(opinion,"span.user-post__published > time:nth-child(2)", "datetime"),
        "useful" : get_element(opinion, "button.vote-yes", "data-total-vote"),
        "unuseful" : get_element(opinion, "button.vote-no > span"),
        "content" : get_element(opinion,"div.user-post__text"),
        "cons" : [cons.text.strip()for cons in opinion.select_one("div.review-feature__title--negatives ~ div.review-feature__item").text.strip()],
        "pros" : [pros.text.strip() for pros in opinion.select_one("div.review-feature__title--positives ~ div.review-feature__item").text.strip()],

    }
    all_opinions.append(single_opinion)
print(all_opinions)
    