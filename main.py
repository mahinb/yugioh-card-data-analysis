########################################################################################################################
#   Algorithm:
#       Prompt the user to enter the filename containing card data.
#       Read the card data from the file using CSV parsing.
#       Enter while loop and present a menu to the user with options to check all cards,
#       search for cards, view decklists, or exit.
#       Perform the corresponding action based on the user's choice.
#       Display statistics and information about cards based on user actions.
#       Repeat the menu loop until the user chooses to exit.
########################################################################################################################

import csv
from operator import itemgetter


MENU = "\nYu-Gi-Oh! Card Data Analysis" \
           "\n1) Check All Cards" \
           "\n2) Search Cards" \
           "\n3) View Decklist" \
           "\n4) Exit" \
           "\nEnter option: "

CATEGORIES = ["id", "name", "type", "desc", "race", "archetype", "card price"]

def open_file(prompt_str):
    '''
    Open a file and return the file pointer.
    prompt_str: A string prompting the user for the file name (str)
    Returns:
    fp: File pointer of the opened file (file object)
    '''
    while True:
        try:
            filename = input(prompt_str)
            fp = open(filename, "r", encoding="utf-8")
            return fp
        except FileNotFoundError:
            print("\nFile not Found. Please try again!")


def read_card_data(fp):
    '''
    Read card data from a CSV file and return a sorted list of card data tuples.
    fp: File pointer of the CSV file containing card data (file object)
    Returns:
    card_data: List of tuples containing card data (list)
    '''
    card_data = []
    reader = csv.reader(fp) #reading csv file
    next(reader, None)
    for column in reader:
        card_id = column[0]
        name = column[1][:45] #limit name to first 45 characters
        type = column[2]
        desc = column[3]
        race = column[4]
        archetype = column[5]
        price = float(column[6])
        card_tuple = (card_id, name, type, desc, race, archetype, price)
        card_data.append(card_tuple)
    # sort first by price, but if price is the same then sort by name
    card_data = sorted(card_data, key=itemgetter(6,1))
    return card_data


def read_decklist(fp, card_data):
    '''
    Read decklist data from a file and return a sorted list of card data tuples.
    fp: File pointer of the decklist file (file object)
    card_data: List of tuples containing card data (list)
    Returns:
    decklist: List of tuples containing decklist data (list)
    '''
    decklist = []
    card_ids = [line.strip() for line in fp]
    for card_id in card_ids:
        for card_tuple in card_data:
            if card_tuple[0] == card_id: #checking if card id in card_data matches card_id in deck
                decklist.append(card_tuple)
                break
    decklist = sorted(decklist, key=itemgetter(6,1))
    return decklist



def search_cards(card_data, query, category_index):
    '''
    Search for cards based on a query and category index.
    card_data: List of tuples containing card data (list)
    query: Search query entered by the user (str)
    category_index: Index of the category to search within card data (int)
    Returns:
    cards: List of tuples containing search results (list)
    '''
    # creates a list of cards that match the query
    cards = [card for card in card_data if query in card[category_index]]
    cards = sorted(cards, key= itemgetter(6,1))
    return cards

def compute_stats(card_data):
    '''
    Compute statistics on card prices.
    card_data: List of tuples containing card data (list)
    Returns:
    min_price_cards: List of tuples containing cards with minimum price (list)
    min_price: Minimum price among all cards (float)
    max_price_cards: List of tuples containing cards with maximum price (list)
    max_price: Maximum price among all cards (float)
    med_price_cards: List of tuples containing cards with median price (list)
    med_price: Median price among all cards (float)
    '''
    prices = [card[6] for card in card_data]
    min_price = min(prices)
    max_price = max(prices)
    med_price = prices[len(card_data)//2] #finds median price. if card_data is even, chooses the higher price
    #creating lists for cards of min,max,and median price
    min_price_cards = [card for card in card_data if card[6] == min_price]
    max_price_cards = [card for card in card_data if card[6] == max_price]
    med_price_cards = [card for card in card_data if card[6] == med_price]
    return min_price_cards, min_price, max_price_cards, max_price, med_price_cards, med_price



def display_data(card_data):
    '''
    Display card data in a tabular format.
    card_data: List of tuples containing card data (list)
    '''
    print(f"{'Name':<50} {'Type':<30} {'Race':<20} {'Archetype':<40} {'TCGPlayer':<12}")
    tot_price = 0
    for card in card_data:
        name = card[1]
        type = card[2]
        race = card[4]
        archetype = card[5]
        price = '{:,.2f}'.format(card[6]) #format the price 2 floating points and add a comma if in thousands
        print(f"{name:<50} {type:<30} {race:<20} {archetype:<40} {price:>12}")
        tot_price += card[6]
    tot_price_format = '{:,.2f}'.format(tot_price)
    print(f"\n{'Totals':<50} {'':<30} {'':<20} {'':<40} {tot_price_format:>12}")


def display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price):
    '''
    Display statistics about card prices.
    min_cards: List of tuples containing cards with minimum price (list)
    min_price: Minimum price among all cards (float)
    max_cards: List of tuples containing cards with maximum price (list)
    max_price: Maximum price among all cards (float)
    med_cards: List of tuples containing cards with median price (list)
    med_price: Median price among all cards (float)
    '''
    print(f"\nThe price of the least expensive card(s) is {'{:,.2f}'.format(min_price)}")
    #print only name of cards
    for card in min_cards:
        print("\t{}".format(card[1]))
    print(f"\nThe price of the most expensive card(s) is {'{:,.2f}'.format(max_price)}")
    for card in max_cards:
        print("\t{}".format(card[1]))
    print(f"\nThe price of the median card(s) is {'{:,.2f}'.format(med_price)}")
    for card in med_cards:
        print("\t{}".format(card[1]))

def main():
    prompt = "\nEnter cards file name: "
    fp = open_file(prompt)
    card_data = read_card_data(fp)
    fp.close()
    while True: #enter while loop until user wants to exit
        option = input(MENU)
        if option == "1":
            print("\nThere are {} cards in the dataset.".format(len(card_data)))
            #check if length of card data exceeds 50, and if it does then only print the first 50
            if len(card_data) > 50:
                display_data(card_data[:50])
            else:
                display_data(card_data)
            min_cards, min_price, max_cards, max_price, med_cards, med_price = compute_stats(card_data)
            display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price)
        elif option == "2":
            query = input("\nEnter query: ")
            category = input("\nEnter category to search: ").lower()
            #check if category is valid and print error message and reprompt if not
            while category not in CATEGORIES:
                print("\nIncorrect category was selected!")
                category = input("\nEnter category to search: ").lower()
            #find what index corresponds to the chosen category
            category_index = CATEGORIES.index(category)
            searched_data = search_cards(card_data, query, category_index)
            print("\nSearch results")
            #check if searched_data contains anything in the list
            if searched_data:
                print("\nThere are {} cards with '{}' in the '{}' category."
                      .format(len(searched_data), query, category))
                display_data(searched_data)
                min_cards, min_price, max_cards, max_price, med_cards, med_price = compute_stats(searched_data)
                display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price)
            else:
                print("\nThere are no cards with '{}' in the '{}' category.".format(query, category))
        elif option == "3":
            prompt = "\nEnter decklist filename: "
            fp = open_file(prompt)
            decklist = read_decklist(fp,card_data)
            fp.close()
            print("\nSearch results")
            display_data(decklist)
            min_cards, min_price, max_cards, max_price, med_cards, med_price = compute_stats(decklist)
            display_stats(min_cards, min_price, max_cards, max_price, med_cards, med_price)
        elif option == "4":
            #breaks the loop when user wants to exit
            break
        else:
            #print error message if option input isnt "1","2","3", or "4"
            print("Invalid option. Please try again!")
    #exit message
    print("\nThanks for your support in Yu-Gi-Oh! TCG")


if __name__ == "__main__":
    main()

