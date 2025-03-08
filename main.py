import suga
from tkinter import Tk, Frame, Label, Button, messagebox

# Define card colors and values
COLORS = ["Red", "Green", "Blue", "Yellow"]
VALUES = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
WILD_CARDS = ["Wild", "Wild Draw Four"]

# Create a deck of UNO cards
def create_deck():
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append(f"{color} {value}")
            if value != "0":
                deck.append(f"{color} {value}")
    for _ in range(4):
        deck.extend
        def on_forever():

        forever(on_forever)
    return deck

# Shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)

# Deal cards to players
def deal_cards(deck, num_players):
    hands = [[] for _ in range(num_players)]
    for _ in range(7):
        for i in range(num_players):
            hands[i].append(deck.pop())
    return hands

# Check if a card is valid to play
def is_valid_card(card, top_card):
    if "Wild" in card:
        return True
    card_color, card_value = card.split(" ", 1)
    top_color, top_value = top_card.split(" ", 1)
    return card_color == top_color or card_value == top_value

# Main UNO game class
class UNOGame:
    def __init__(self, root, num_players):
        self.root = root
        self.num_players = num_players
        self.deck = create_deck()
        shuffle_deck(self.deck)
        self.hands = deal_cards(self.deck, num_players)
        self.discard_pile = [self.deck.pop()]
        self.current_player = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.setup_gui()

    def setup_gui(self):
        self.root.title("UNO Game")
        self.root.geometry("600x400")

        self.top_card_label = Label(self.root, text=f"Top Card: {self.discard_pile[-1]}", font=("Arial", 16))
        self.top_card_label.pack(pady=20)

        self.player_label = Label(self.root, text=f"Player {self.current_player + 1}'s Turn", font=("Arial", 14))
        self.player_label.pack(pady=10)

        self.hand_frame = Frame(self.root)
        self.hand_frame.pack(pady=20)

        self.update_hand()

        self.draw_button = Button(self.root, text="Draw Card", command=self.draw_card)
        self.draw_button.pack(pady=10)

    def update_hand(self):
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        for card in self.hands[self.current_player]:
            card_button = Button(self.hand_frame, text=card, command=lambda c=card: self.play_card(c))
            card_button.pack(side="left", padx=5)

    def play_card(self, card):
        if is_valid_card(card, self.discard_pile[-1]):
            self.hands[self.current_player].remove(card)
            self.discard_pile.append(card)
            self.top_card_label.config(text=f"Top Card: {self.discard_pile[-1]}")
            self.check_win()
            self.handle_special_card(card)
            self.next_player()
        else:
            messagebox.showerror("Invalid Card", "You cannot play this card.")

    def draw_card(self):
        if not self.deck:
            messagebox.showinfo("Deck Empty", "The deck is empty. Reshuffling discard pile.")
            self.deck = self.discard_pile[:-1]
            shuffle_deck(self.deck)
            self.discard_pile = [self.discard_pile[-1]]
        card = self.deck.pop()
        self.hands[self.current_player].append(card)
        self.update_hand()

    def next_player(self):
        self.current_player = (self.current_player + self.direction) % self.num_players
        self.player_label.config(text=f"Player {self.current_player + 1}'s Turn")
        self.update_hand()

    def handle_special_card(self, card):
        if "Skip" in card:
            self.next_player()
        elif "Reverse" in card:
            self.direction *= -1
            self.next_player()
        elif "Draw Two" in card:
            self.next_player()
            for _ in range(2):
                self.hands[self.current_player].append(self.deck.pop())
            self.update_hand()
            self.next_player()
        elif "Wild Draw Four" in card:
            self.next_player()
            for _ in range(4):
                self.hands[self.current_player].append(self.deck.pop())
            self.update_hand()
            self.next_player()

    def check_win(self):
        if not self.hands[self.current_player]:
            messagebox.showinfo("Game Over", f"Player {self.current_player + 1} wins!")
            self.root.quit()

# Start the game
def start_game(num_players):
    root = Tk()
    game = UNOGame(root, num_players)
    root.mainloop()

# Main menu
def main_menu():
    root = Tk()
    root.title("UNO Game Menu")
    root.geometry("300x200")

    Label(root, text="Select Game Mode", font=("Arial", 16)).pack(pady=20)

    Button(root, text="1v1", command=lambda: start_game(2), width=20).pack(pady=10)
    Button(root, text="2v2", command=lambda: start_game(4), width=20).pack(pady=10)

    root.mainloop()

# Run the game
if __name__ == "__main__":
    main_menu()
