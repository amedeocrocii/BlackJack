import random


def create_deck():
    """
    Creates a standard deck of 52 playing cards and duplicates it to form a double-deck.
    :return: returns the deck
    """
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    single_deck = [{"value": value, "suit": suit} for suit in suits for value in values]
    deck = single_deck * 2
    return deck


def shuffle_deck(deck):
    """
    Shuffles randomly the double-deck of cards.
    :param deck: the double-deck of cards to be shuffled
    :return: returns the double-deck of cards randomly shuffled
    """
    random.shuffle(deck)


def deal_card(deck):
    """
    It deals the card on top of the double-deck, removing it.
    :param deck: the shuffled double-deck
    :return: the dealt card
    """
    return deck.pop()


def card_value(card):
    """
    Determines the value of a card so that every card has its face value except for J,Q,K which are worth 10.
    The funciton also makes the ace value 11. We'll later adjust it so that it is worth 1 when ,
    :param card: a list representing the deck of cards from which the first is removed
    :return: the removed card represented as a dictionary containing a value and suit
    """
    value = card["value"]
    if value in ["J", "Q", "K"]:
        return 10
    elif value == "A":
        return 11
    else:
        return int(value)


def calculate_total(hand, has_hit_after_ace=False):
    """
    It calculates the value of a hand by summing the values of the cards drawn.
    Aces are handled differently depending on whether they'll be worth either 1 or 11
    this is done by first counting the number of aces and then adjusted
    if the player stays and the value of the cards doesn't exceed 21 the card is valued at 11
    :param hand: a list of dictionaries representing the player's hand, each containing a value and suit
    :param has_hit_after_ace: a flag to track if the player has hit after obtaining an Ace
    :return: the total value of the hand adjusted for aces if necessary
    """
    total = 0
    aces = 0

    for card in hand:
        value = card["value"]
        total += card_value(card)
        if value == "A":
            aces += 1

    if has_hit_after_ace:
        total -= aces * 10  #
    else:
        while total > 21 and aces:
            total -= 10
            aces -= 1

    return total


def display_hand(hand):
    """
    Generates a string representation of a hand of cards in a readable way.
    :param hand: a list of dictionaries of cards with a value and a suit
    :return: a string that lists the cards in the hand in the format "value of suit"
    """
    return ", ".join(f"{card['value']} of {card['suit']}" for card in hand)


def main():
    """
    function starts by asking player how much they're willing to wager
    then asks what portion of wager they want to play for round
    deck is then shuffled and both dealer and player recieve a card each
    both players cards are shown
    then player, without seeing dealers second card, can either hit or stay
    player can keep hitting until total value of their cards exceed 21
    however if players hits 21 they get blackjack and 2.5x the amount they played for that round
    dealer draws their second card; only while total card value for them is below 17
    after player either goes bust or wins, dealers hand is revealed therefore announcing the winner of the round
    """
    print("Welcome to Blackjack! I am SkibidiAhmed, your dealer for today.")  # Fixed the missing closing quote

    while True:
        buy_in = input("How much would you like to buy in for? ").strip()
        try:
            player_money = int(buy_in)
            if player_money > 0:
                break
            else:
                print("Hey if you don't have money just leave!")
        except ValueError:
            print("Please buy in for a valid amount. Don't waste my time!")

    while player_money > 0:
        print(f"\nYour balance is {player_money} euros.")
        bet_input = input("Place your bet (or type 'cashout' to leave the table): ").strip()
        if bet_input.lower() == "cashout":
            break
        try:
            bet = int(bet_input)
        except ValueError:
            print("Invalid bet. Please enter a valid number and stop wasting my time.")
            continue

        if bet <= 0 or bet > player_money:
            print("Bet must be a positive number not exceeding your current money.")
            continue

        deck = create_deck()
        shuffle_deck(deck)

        player_hand = [deal_card(deck)]
        dealer_hand = [deal_card(deck)]

        print("\nDealer's hand:", display_hand(dealer_hand),
              "and a hidden card (Total: {})".format(calculate_total(dealer_hand)))
        print("Your hand:", display_hand(player_hand), f"(Total: {calculate_total(player_hand)})")

        while True:
            move = input("Do you want to hit or stay? ").strip().lower()
            if move not in ["hit", "stay"]:
                print("Please choose either 'hit' or 'stay'. Don't waste my time!")
                continue

            if move == "hit":
                card = deal_card(deck)
                player_hand.append(card)
                total = calculate_total(player_hand)
                print("\nYou were dealt:", f"{card['value']} of {card['suit']}")
                print("Your hand:", display_hand(player_hand), f"(Total: {total})")
                if total > 21:
                    print("Bust! You exceeded 21.")
                    break
                elif total == 21:
                    print("It's your lucky day. You hit 21!")
                    break
            else:
                break

        player_total = calculate_total(player_hand)
        if player_total > 21:
            print("I'm sorry. You busted! You lose your bet.")
            player_money -= bet
            continue

        if len(player_hand) == 2 and player_total == 21:
            print("Lucky one! Blackjack! You win 2.5x your bet!")
            player_money += int(bet * 2.5)
            continue

        print("\nDealer's turn...")
        dealer_total = calculate_total(dealer_hand)
        print("Dealer's starting hand:", display_hand(dealer_hand), f"(Total: {dealer_total})")

        while dealer_total < 17:
            card = deal_card(deck)
            dealer_hand.append(card)
            dealer_total = calculate_total(dealer_hand)
            print("Dealer draws:", f"{card['value']} of {card['suit']}")
            print("Dealer's hand:", display_hand(dealer_hand), f"(Total: {dealer_total})")
            if dealer_total > 21:
                break

        print("\nFinal totals:")
        print("Your total:", player_total)
        print("Dealer's total:", dealer_total)

        if dealer_total > 21:
            print("Dealer busts! You win!")
            player_money += bet
        else:
            if player_total > dealer_total:
                print("You win!")
                player_money += bet
            elif player_total < dealer_total:
                print("Dealer wins. You lose your bet.")
                player_money -= bet
            else:
                print("Push! It's a tie. Your bet is returned.")

        print("Round over. Your current total is", player_money, "euros.")

    print("\nYour cash out is", player_money,
          "euros. \nIt was a pleasure dealing for you today! \nHave a great day and come back soon!")


main()