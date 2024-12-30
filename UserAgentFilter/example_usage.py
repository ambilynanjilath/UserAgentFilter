from selector import GetUserAgent
from tester  import UserAgentTester
import requests
from bs4 import BeautifulSoup

def scrape_amazon_product_links(url, headers):
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch page: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        product_links = []

        # Find all product link elements using their unique class or attribute
        for a_tag in soup.select("a.a-link-normal.s-line-clamp-2"):
            link = a_tag.get("href")
            if link and "/dp/" in link:  # Ensure it's a valid product link
                product_links.append(f"https://www.amazon.in{link}")

        return product_links

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []



# Initialize the GetUserAgent class with the file path to user agents
user_agent_selector = GetUserAgent(file_path="UserAgentFilter/text_file/user_agents.txt")

# Define Amazon URLs to scrape
urls = [
    "https://www.amazon.in/s?i=apparel&bbn=1968062031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968062031%2Cn%3A1968073031%2Cp_85%3A10440599031%2Cp_89%3AASICs%257CAdidas%257CCALVINKLEIN%257CCHKOKKO%257CCK%2BCALVIN%2BKLEIN%257CCK%2BCalvin%2BKlein%257CCalvin%2BKlein%257CCalvin%2BKlein%2BJeans%257CColumbia%257CJockey%257CNike%257CPuma%257CReebok%257CTommy%2BHilfiger%257CUnder%2Barmour&s=apparel&dc&ds=v1%3AWCTW4Vl0gT0rIS6vG44c5H2cVMRNzS%2BJxyz5FnnDz5U&pf_rd_i=12456568031&pf_rd_i=14153691031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7a317334-3730-427b-9cf4-b87d7dbfb528&pf_rd_p=cc538c73-ebe4-456f-9700-4297565f0537&pf_rd_r=5Z7E0YT6WWAF6M1205VD&pf_rd_r=C3KANTZHJBF9YSJ2FCC9&pf_rd_s=merchandised-search-10&pf_rd_s=merchandised-search-8&qid=1668515581&rnid=1968062031&ref=sr_nr_n_1",
    "https://www.amazon.in/s?i=apparel&bbn=1968062031&rh=n%3A1571271031%2Cn%3A1968024031%2Cn%3A1968062031%2Cn%3A1968068031%2Cp_85%3A10440599031%2Cp_89%3AASICs%257CAdidas%257CCALVINKLEIN%257CCHKOKKO%257CCK%2BCALVIN%2BKLEIN%257CCK%2BCalvin%2BKlein%257CCalvin%2BKlein%257CCalvin%2BKlein%2BJeans%257CColumbia%257CJockey%257CNike%257CPuma%257CReebok%257CTommy%2BHilfiger%257CUnder%2Barmour&s=apparel&dc&ds=v1%3AzjDunqC7eYyr%2BRIZQ6tNI1Hg%2FzfOc%2F6XNi5%2Fh75MN8k&pf_rd_i=12456568031&pf_rd_m=A1VBAL9TL5WCBF&pf_rd_p=7a317334-3730-427b-9cf4-b87d7dbfb528&pf_rd_r=504GX6HWEXB5WTP6D7CB&pf_rd_s=merchandised-search-10&qid=1668509905&rnid=1968062031&ref=sr_nr_n_3"
]

# Define the number of user agents to test
number_of_agents = 5

# Select and test user agents
user_agent_selector.test_user_agents(number=number_of_agents, test_url=urls[0])

# Scrape product links from each URL using random successful user agents
for url in urls:
    headers = {
        "User-Agent": user_agent_selector.get_random_user_agent()
    }
    product_links = scrape_amazon_product_links(url, headers)
    print(f"Scraped {len(product_links)} product links from {url}")
