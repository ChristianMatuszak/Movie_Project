import json

DATA_FILE = "data.json"

def get_movies():
    """
    Loads the movie database from the JSON file.
    This function reads the `data.json` file and returns the movie data as a dictionary. 
    If the file does not exist or cannot be read, it returns an empty dictionary.
    :return: dict
            A dictionary where keys are movie titles (strings) and values are dictionaries
            containing movie details such as 'year' and 'rating'.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_movies(movies):
    """
    Saves the movie database to the JSON file.
    This function writes the given movie dictionary to `data.json` in JSON format.
    :param movies: dict
        A dictionary where keys are movie titles (strings) and values are dictionaries
        containing movie details such as 'year' and 'rating'.
    :return: None
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(movies, file, indent=4)

def add_movie(title, year, rating):
    """
    Adds a new movie to the database and saves the updated list.
    This function adds a new movie with the given title, year, and rating to the 
    movie database and updates the JSON file.
    :param title: str : The title of the movie to add.
    :param year: int : The release year of the movie.
    :param rating: float : The rating of the movie.
    :return: None
    """
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)
    print(f"Movie '{title}' added successfully.")

def update_movie(title, year=None, rating=None):
    """
    Updates an existing movie's details in the database.
    This function updates the year and/or rating of a specified movie. If a parameter 
    is not provided, the existing value remains unchanged.
    :param title: str: The title of the movie to update.
    :param year: int, optional: The new release year of the movie (if updating).
    :param rating: float, optional: The new rating of the movie (if updating).
    :return: None
    """
    movies = get_movies()
    if title in movies:
        if year is not None:
            movies[title]["year"] = year
        if rating is not None:
            movies[title]["rating"] = rating
        save_movies(movies)
        print(f"Movie '{title}' updated successfully.")
    else:
        print(f"Movie '{title}' not found in the database.")

def delete_movie(title):
    """
    Deletes a movie from the database.
    This function removes a specified movie from the movie database and updates the JSON file.
    :param title: str: The title of the movie to delete.
    :return: None
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)
        print(f"Movie '{title}' deleted successfully.")
    else:
        print(f"Movie '{title}' not found in the database.")
