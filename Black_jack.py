import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

class Card:
    
    def __init__(self,suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        for i in self.deck:
            print(i)
        return '0'

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self):
        self.value = 0
        for i in self.cards:
            self.value = self.value + values[i.rank]
    
    def __str__(self):
        for i in self.cards:
            print(i)
        return '0'

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total = self.total + self.bet
    
    def lose_bet(self):
        self.total = self.total - self.bet

def take_bet():
    while True:
        try:
            bet = int(input("Enter your bet (In multiple of 10): "))
        except:
            print("Whoops! that is not a number.\n")
            continue
        else:
            if bet%10 != 0:
                print("That is not multiple of 10!\n")
                continue
            else:
                break
    return bet

def hit(deck,hand):
    c = deck.deal()
    hand.cards.append(c)
    hand.add_card()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        prompt = input("Hit or stand (Enter 'h' for Hit and 's' for stand): ")
        if prompt == 'h':
            hit(deck,hand)
            break
        elif prompt == 's':
            playing = False
            break
        else:
            continue 

def show_some(player,dealer):
    print("Player's hand")
    print(player)
    print('\n')
    print("dealer's hand")
    d1 = dealer.cards[0]
    print(d1)
    print("*2nd card hidden*\n")
    
def show_all(player,dealer):
    print("Player's hand")
    print(player)
    print('\n')
    print("dealer's hand")
    print(dealer)


#winning scenarios
def player_busts(player, cplayer, cdealer):
    if player.value > 21:
        cplayer.lose_bet()
        cdealer.win_bet()
        return True
    else:
        return False

def player_wins(dealer, player, cplayer, cdealer):
    if dealer.value < player.value or player.value == 21:
        cplayer.win_bet()
        cdealer.lose_bet()
        return True
    else:
        return False

def dealer_busts(dealer, cplayer, cdealer):
    if dealer.value > 21:
        cplayer.win_bet()
        cdealer.lose_bet()
        return True
    else:
        return False
    
def dealer_wins(dealer, player, cplayer, cdealer):
    if dealer.value > player.value or dealer.value == 21:
        cplayer.lose_bet()
        cdealer.win_bet()
        return True
    else:
        return False
    
def push(dealer, player):
    if dealer.value == player.value:
        return True
    else:
        return False


# Main function
# Print an opening statement
print("\t\t\t\t *Welcome to Black Jack game*")
print("1. Player has 100 chips available")
print("2. Player can only bet chips in multiple of 10\n")

# Set up the Player's chips
chips_player = Chips()
chips_dealer = Chips()

while True: 
    playing = True
    # Create & shuffle the deck, deal two cards to each player
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
        
    player.cards.append(deck.deal())
    player.cards.append(deck.deal())
    dealer.cards.append(deck.deal())
    dealer.cards.append(deck.deal())
    player.add_card()
    dealer.add_card()
    
   
    # Prompt the Player for their bet
    bet = take_bet()
    chips_player.bet =  bet
    chips_dealer.bet =  bet
    print('\n')
    
    # Show cards (but keep one dealer card hidden)
    show_some(player,dealer)
    if player.value == 21:
        chips_player.win_bet()
        chips_dealer.lose_bet()
        print("\nPlayer wins. Their total chips are {} \n".format(chips_player.total))
        y = input("Do you want to play again? 'y or 'n': ")
        if y=='y':
	        continue
        else:
	        break            

    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player)
        if playing == False:
            break
        
        
        # Show cards (but keep one dealer card hidden)
        show_some(player,dealer)
        print(player.value) 
        z = False
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player, chips_player, chips_dealer):
            z = True
            print("\nPlayer has busted and loses bet to dealer and their total chips are {}. \nThanks for playing".format(chips_player.total))
            break
        else:
            continue
    
    if z:
        if chips_player.total >= 20:
	        y = input("Do you want to play again? 'y or 'n': ")
	        if y == 'y':
	            continue
	        else:
	            break
        else:
            print("Player don't have enough chips to play! please come when you have money.")
            break
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if not player_busts(player, chips_player, chips_dealer):
        show_all(player,dealer)  # Show all cards
        
        # Running different winning scenarios                
        if dealer_wins(dealer, player, chips_player, chips_dealer):
            print("\n Player loses bet to dealer and their total chips are {}. \nThanks for playing".format(chips_player.total))
            if chips_player.total >= 20:
	            y = input("Do you want to play again? 'y or 'n': ")
	            if y == 'y':
	            	continue
	            else:
	            	break
            else:
                print("Player don't have enough chips to play! please come when you have money.")
                break
        
        while dealer.value < 17:
            hit(deck, dealer)
        
        show_all(player,dealer)
        
        if dealer_busts(dealer, chips_player, chips_dealer):
            print("\n Player wins and their total chips are {}.\nThanks for playing".format(chips_player.total))
            y = input("Do you want to play again? 'y or 'n': ")
            if y == 'y':
                continue
            else:
                break
        
        if dealer_wins(dealer, player, chips_player, chips_dealer):
            print("\n Player loses bet to dealer and their total chips are {}. \nThanks for playing".format(chips_player.total))
            if chips_player.total >= 20:
                y = input("Do you want to play again? 'y or 'n': ")
                if y == 'y':
                    continue
                else:
                    break
            else:
                print("Player don't have enough chips to play! please come when you have money.")
                break
                        
        if player_wins(dealer, player, chips_player, chips_dealer):
            print("\n Player wins and their total chips are {}.\nThanks for playing".format(chips_player.total))
            y = input("Do you want to play again? 'y or 'n': ")
            if y == 'y':
                continue
            else:
                break
                
        if push(dealer, player):
            print('its a tie!')
            y = input("Do you want to play again? 'y or 'n': ")
            if y == 'y':
                continue
            else:
                break

p = input("\nPress any key to exit")