import os
import requests
import logging
import re
from bs4 import BeautifulSoup


def search_movie(movie_title):
    # Format the movie title for the IMDb search URL
    formatted_title = movie_title.replace(" ", "+")
    search_url = f"https://www.imdb.com/find?q={formatted_title}&s=tt&ttype=ft&ref_=nv_sr_sm"

    # Send a GET request to the IMDb search page
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first search result (movie) on the search page
    result = soup.find("td", class_="result_text")
    if result:
        # Extract the movie's URL
        movie_url = "https://www.imdb.com" + result.a["href"]

        # Send a GET request to the movie's page
        movie_response = requests.get(movie_url)
        movie_soup = BeautifulSoup(movie_response.content, "html.parser")

        # Extract the movie's rating and summary
        rating = movie_soup.find("span", itemprop="ratingValue")
        summary = movie_soup.find("div", class_="summary_text")

        if rating and summary:
            return rating.text.strip(), summary.text.strip()
        else:
            return None, None
    else:
        return None, None


def extract_movie_name(folder_name):
    # Remove extra information from the folder name using regular expressions
    # Assuming the movie name is followed by the year in parentheses
    # Example: "A Hidden Life (2019) [720p] [WEBRip] [YTS.MX]"
    pattern = r"^(.*?)\s?\(\d{4}\)"
    match = re.search(pattern, folder_name)
    if match:
        return match.group(1).strip()
    else:
        return folder_name


def main(directory, log_file):
    # Configure logging to write to the log file
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Get the list of folder names in the directory
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    for folder_name in folders:
        movie_name = extract_movie_name(folder_name)
        logging.info("Movie: %s", movie_name)
        rating, summary = search_movie(movie_name)
        if rating and summary:
            logging.info("Rating: %s", rating)
            logging.info("Summary: %s", summary)
        else:
            logging.info("No movie found with a similar name on IMDb")


if __name__ == "__main__":
    directory = input("Enter the source folder path : \n")
    # D:\Movies
    log_file = "movie_log.txt"  # Replace with the desired log file path
    # directory = "/path/to/your/directory"  # Replace with the desired directory path
    main(directory, log_file)
