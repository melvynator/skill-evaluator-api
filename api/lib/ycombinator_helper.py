from bs4 import BeautifulSoup
from api.models.ycombinator_job import YcombinatorJob
from api.models.offering_page import OfferingPage
import datetime
import re


def get_offering_pages(whoishiring_content):
    soup = BeautifulSoup(whoishiring_content, "html.parser")
    posts = soup.find_all("tr", {"class": "athing"})
    links = list(map(lambda post: post.find("a", {"class": "storylink"}), posts))
    whoishiring_links = list(filter(lambda link: "hiring?" in link.text.lower(), links))
    whoishiring_pages = list(map(lambda link: OfferingPage(link["href"], extract_date(link.text)), whoishiring_links))
    return whoishiring_pages


def extract_date(title):
    regex = re.compile(r"\((.*?)\)")
    date_str = regex.search(title)
    datetime_object = datetime.datetime.strptime(date_str.group(1), '%B %Y')
    return datetime_object


def get_page_data(page_content, month):
    soup = BeautifulSoup(page_content, 'html.parser')
    posts = soup.find_all("tr", {"class": "athing comtr "})
    posts = [post for post in posts if post.find("img", {"src": "s.gif", "width": "0"})]
    users = [post.find("a", {"class": "hnuser"}).text if post.find("a", {"class": "hnuser"}) else "DELETED" for post in posts]
    clean_posts = [post.find("div", {"class": "comment"}).getText(separator=' ').replace("\n", " ") for post in posts]
    ycombinator_jobs = list(map(YcombinatorJob.from_crawler, users, clean_posts, [month]*len(users)))
    return ycombinator_jobs


def get_next_page(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    next_page = soup.find("a", {"class": "morelink"})
    if next_page:
        return next_page["href"]
    else:
        return None
