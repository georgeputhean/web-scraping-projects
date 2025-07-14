import requests
from bs4 import BeautifulSoup

def main():
    topic_url = "https://github.com/topics"
    response = requests.get(topic_url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page {topic_url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Let's try to find the container for all the topics
    container = soup.find("div", class_="container-lg p-responsive mt-6")
    print("Container found:", bool(container))

    # Now let's see if we can find the topic titles within the container
    if container:
        # Looking for all 'p' tags to see what we get
        all_p_tags = container.find_all('p')
        print(f"Found {len(all_p_tags)} 'p' tags.")
        for tag in all_p_tags:
            print(tag)
            print("-" * 20)


if __name__ == "__main__":
    main()
