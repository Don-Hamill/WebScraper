def nature_scraper():
    page_range = int(input("Enter the page range: "))
    article_type = input("Enter the article type: ")
    directory = os.getcwd()
    for i in range(1, page_range + 1):
        r = requests.get(f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={i}")
        soup = BeautifulSoup(r.content, "html.parser")
        articles = soup.find_all("article")
        for j in articles:
            news = j.find('span', class_="c-meta__type")
            if article_type in news:
                find_link = j.find('a')  # {'data-track-action': 'view article'})
                tail = find_link.get('href')
                new_link = "https://www.nature.com" + tail
                r_sub = requests.get(new_link, headers={'Accept-Language': 'en-US,en;q=0.5'})
                soup_2 = BeautifulSoup(r_sub.content, 'html.parser')
                title = soup_2.find("title").text.strip()

                # removing punctuation
                table = str.maketrans(dict.fromkeys(string.punctuation))
                table2 = title.translate(table)

                # replacing spaces by _
                final_title = table2.translate(title.maketrans(' ', '_'))

                # Creating directory if it doesn't exist
                os.makedirs(directory + f"\Page_{i}", exist_ok=True)
                os.chdir(directory + f"\Page_{i}")

                # saving txt files that don't contain 'images' title html tag
                if 'images' not in title:
                    try:
                        body = soup_2.find('div', class_="article__body").text.strip()
                        file = open(f"{final_title.replace('__Research_Highlights', '')}.txt", "w", encoding="utf-8")
                        file.write(body)
                        file.close()
                        os.chdir(directory)

                    except AttributeError:
                        body = soup_2.find('div', class_="article-item__body").text.strip()
                        file = open(f"{final_title.replace('__Research_Highlights', '')}.txt", "w", encoding="utf-8")
                        file.write(body)
                        file.close()
                        os.chdir(directory)
            # create empty folder if article type not on page
            elif article_type not in news:
                os.makedirs(directory + f"\Page_{i}", exist_ok=True)
                os.chdir(directory)

    print("Saved all articles.")


nature_scraper()