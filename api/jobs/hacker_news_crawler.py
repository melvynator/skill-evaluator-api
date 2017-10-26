import requests
import time
from api import YCOMBINATOR
from api import WHOISHIRING_SEED
from api import HEADER
from api import es
from api.lib.ycombinator_helper import get_offering_pages, get_next_page, get_page_data
from api.lib.helper import create_index

seed = WHOISHIRING_SEED
next_page = seed
pages = []
print("Collecting page")
while next_page:
    print(next_page)
    response = requests.get(YCOMBINATOR + next_page, headers=HEADER)
    response_content = response.content
    pages = pages + get_offering_pages(response_content)
    next_page = get_next_page(response_content)
    time.sleep(30)

print(len(pages), "has been collected")
print("Collecting data")

create_index(es, "jobs", "jobs")
pages = pages[23:]
for index, page in enumerate(pages):
    seed = page.link
    next_page = seed
    while next_page:
        print("Page: {0}, {1}".format(index, next_page))
        response = requests.get(YCOMBINATOR + next_page, headers=HEADER)
        if response.status_code != 200:
            print(YCOMBINATOR + next_page)
            print("Error while crawling")
            break
        else:
            page_content = response.content
            jobs = get_page_data(page_content, page.date.strftime('%B %Y'))
            for job in jobs:
                print(job)
                job.save_to_es()
            next_page = get_next_page(page_content)
            time.sleep(30)
