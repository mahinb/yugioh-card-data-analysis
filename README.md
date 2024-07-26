
# Yu-Gi-Oh! Card Data Analysis
# Overview
This Python application allows users to analyze Yu-Gi-Oh! card data from CSV files and deck data from YDK files. It provides functionalities to check all cards, search for specific cards, view decklists, and display various card statistics.

# Features
Check All Cards: Display all card data with sorting and formatting.
Search Cards: Search for cards based on user queries and categories.
View Decklist: Load and analyze decklists from files.
Display Statistics: Compute and display statistics such as minimum, maximum, and median card prices.

# Functions
open_file(prompt_str)
Prompts the user to enter a filename and opens the file.

read_card_data(fp)
Reads and sorts card data from a CSV file.

read_decklist(fp, card_data)
Reads and sorts decklist data from a file, integrating with card data.

search_cards(card_data, query, category_index)
Searches for cards based on a query and category.

compute_stats(card_data)
Computes statistics on card prices, including minimum, maximum, and median prices.

display_data(card_data)
Displays card data in a tabular format.

display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price)
Displays statistics about card prices.

# Menu Options
1) Check All Cards: Display a list of all cards and their statistics.
2) Search Cards: Search for cards based on user input.
3) View Decklist: View and analyze a decklist from a file.
4) Exit: Exit the application.
