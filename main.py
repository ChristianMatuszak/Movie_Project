import random
import sys
import movie_storage
from rapidfuzz import process
from colorama import Fore, Style


def main():
    """
    Runs the interactive movie database application.

    This function presents a menu to the user, allowing them to:
    - List all movies
    - Add a new movie
    - Delete a movie
    - Update movie details
    - View movie statistics
    - Select a random movie
    - Search for a movie
    - Sort movies by rating

    The user can exit the application by selecting option 0.

    :return: None
    """
    while True:
        print("\n********** My Movie Database **********")
        print("\n      Menu:")
        print(Fore.GREEN + "0. " + Style.RESET_ALL + "Exit")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "List movies")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Add movie")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Delete movie")
        print(Fore.GREEN + "4. " + Style.RESET_ALL + "Update movie")
        print(Fore.GREEN + "5. " + Style.RESET_ALL + "Stats")
        print(Fore.GREEN + "6. " + Style.RESET_ALL + "Random movie")
        print(Fore.GREEN + "7. " + Style.RESET_ALL + "Search movie")
        print(Fore.GREEN + "8. " + Style.RESET_ALL + "Movies sorted by rating or year")
        print(Fore.GREEN + "9. " + Style.RESET_ALL + "Filter movie by your criteria")
        print()

        choice = input("Enter choice (0-8): \n")

        if choice == "0":
            print("\nBye!")
            sys.exit()
        elif choice == "1":
            list_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            update_movie()
        elif choice == "5":
            movie_stats()
        elif choice == "6":
            movie, rating, year = random_movie()
            print(f"Your movie for tonight: {movie}, it's rated {rating}. It was released {year}")
        elif choice == "7":
            search_movie()
        elif choice == "8":
            movies_sorted_by()
        elif choice == "9":
            filter_movies()
        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)


def list_movies():
    """Prints all movies in the database."""
    try:
        movies = movie_storage.get_movies()
        if not movies:
            print(Fore.YELLOW + "No movies found in the database." + Style.RESET_ALL)
            return
        for movie, data in movies.items():
            print(f"{movie}: {data['rating']} released: {data['year']}")
    except Exception as e:
        print(Fore.RED + f"Error loading movies: {e}" + Style.RESET_ALL)


def add_movie():
    """Prompts the user to add a movie and updates the database."""
    try:
        movies = movie_storage.get_movies()
        title = input("Enter the name of the movie you want to add: ")

        if title in movies:
            print(Fore.RED + "This movie already exists" + Style.RESET_ALL)
            return

        year = int(input("Enter the release year of the movie: "))
        rating = float(input("Enter the rating of the movie (1.0 to 10.0): "))

        movie_storage.add_movie(title, year, rating)
        print(f"The movie '{title}' was added.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter valid numbers for year and rating." + Style.RESET_ALL)


def delete_movie():
    """Prompts the user to delete a movie and updates the database."""
    try:
        title = input("Enter the movie you want to delete: ")
        movie_storage.delete_movie(title)
    except Exception as e:
        print(Fore.RED + f"Error deleting movie: {e}" + Style.RESET_ALL)


def update_movie():
    """Prompts the user to update a movie's rating and year."""
    try:
        title = input("Enter the movie you want to update: ")
        year = int(input(f"Enter the new release year for {title}: "))
        rating = float(input(f"Enter the new rating for {title} (1.0 to 10.0): "))

        movie_storage.update_movie(title, year, rating)
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter valid numbers for year and rating." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error updating movie: {e}" + Style.RESET_ALL)


def movie_stats():
    """Displays statistical information about the movies."""
    movies = movie_storage.get_movies()

    if not movies:
        print(Fore.RED + "No movies in the database." + Style.RESET_ALL)
        return

    ratings = [data["rating"] for data in movies.values()]
    avg_rating = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    mid = len(sorted_ratings) // 2
    median_rating = sorted_ratings[mid] if len(sorted_ratings) % 2 else (sorted_ratings[mid - 1] + sorted_ratings[
        mid]) / 2

    best = max(movies, key=lambda x: movies[x]["rating"])
    worst = min(movies, key=lambda x: movies[x]["rating"])

    print(f"Average rating: {avg_rating:.2f}")
    print(f"Median rating: {median_rating:.2f}")
    print(f"The best movie: {best} ({movies[best]['rating']})")
    print(f"The worst movie: {worst} ({movies[worst]['rating']})")


def random_movie():
    """Selects a random movie from the database."""
    try:
        movies = movie_storage.get_movies()
        if not movies:
            print(Fore.YELLOW + "No movies in the database." + Style.RESET_ALL)
            return None, None, None

        movie = random.choice(list(movies.keys()))
        return movie, movies[movie]["rating"], movies[movie]["year"]
    except Exception as e:
        print(Fore.RED + f"Error selecting a random movie: {e}" + Style.RESET_ALL)
        return None, None, None


def search_movie():
    """Searches for a movie by name using fuzzy matching."""
    try:
        movies = movie_storage.get_movies()
        search_query = input("Enter the name of the movie to search: ").strip().lower()
        matched_movies = process.extract(search_query, movies.keys(), limit=5)

        relevant_matches = [(match, score) for match, score, _ in matched_movies if score >= 75]

        if relevant_matches:
            print(Fore.CYAN + "Matching movies:" + Style.RESET_ALL)
            for movie, _ in relevant_matches:
                print(f"{movie}: {movies[movie]['rating']} released: {movies[movie]['year']}")
        else:
            print(Fore.RED + "No movies found matching your search." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error searching for a movie: {e}" + Style.RESET_ALL)


def movies_sorted_by():
    """Prints movies sorted by rating or by year (chronologically)."""
    try:
        movies = movie_storage.get_movies()
        if not movies:
            print(Fore.YELLOW + "No movies available." + Style.RESET_ALL)
            return

        print("\nSort movies by:")
        print("1. Rating (Highest to Lowest)")
        print("2. Year (Chronological Order)\n")
        choice = input("Enter your choice (1 or 2): \n").strip()

        if choice == "1":
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        elif choice == "2":
            order = input("Show latest movies first? (y/n): \n").strip().lower()
            reverse_order = order == "y"
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse_order)
        else:
            print(Fore.RED + "Invalid choice. Returning to menu." + Style.RESET_ALL)
            return

        for movie, data in sorted_movies:
            print(f"{movie}: {data['rating']} (Released: {data['year']})")
    except Exception as e:
        print(Fore.RED + f"Error sorting movies: {e}" + Style.RESET_ALL)


def filter_movies():
    """
    Filters the movies based on user-defined criteria: minimum rating, start year, and end year.
    The user can leave any input blank, which means no restriction for that filter.
    The filtered movies are then displayed with their titles, release years, and ratings.
    """
    try:
        movies = movie_storage.get_movies()
        if not movies:
            print(Fore.YELLOW + "No movies available in the database." + Style.RESET_ALL)
            return

        min_rating = input("Enter minimum rating (leave blank for no minimum rating): ").strip()
        start_year = input("Enter start year (leave blank for no start year): ").strip()
        end_year = input("Enter end year (leave blank for no end year): ").strip()

        min_rating = float(min_rating) if min_rating else None
        start_year = int(start_year) if start_year else None
        end_year = int(end_year) if end_year else None

        filtered_movies = {
            title: data for title, data in movies.items()
            if (min_rating is None or data["rating"] >= min_rating) and
               (start_year is None or data["year"] >= start_year) and
               (end_year is None or data["year"] <= end_year)
        }

        if filtered_movies:
            print(Fore.CYAN + "\nFiltered Movies:\n" + Style.RESET_ALL)
            for title, data in sorted(filtered_movies.items(), key=lambda x: x[1]['year']):
                print(f"{title} ({data['year']}): {data['rating']}")
        else:
            print(Fore.RED + "No movies match the given criteria." + Style.RESET_ALL)

    except ValueError:
        print(Fore.RED + "Invalid input. Please enter valid numbers for rating and years." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error filtering movies: {e}" + Style.RESET_ALL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram terminated by user." + Style.RESET_ALL)
