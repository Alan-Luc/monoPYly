import random


class Board:
    def __init__(self):
        self.board = dict()
        self.propertyChoices = {"y", "n"}
        for i in range(40):
            self.board[i] = None

        self.board[3] = Property(3, 200, 50)
        self.board[7] = Property(7, 400, 100)
        self.board[13] = Property(13, 800, 350)

    def handleProperty(self, player):
        currTile = player.location
        if self.board[currTile] is not None:
            property = self.board[currTile]
            if property.owner and property.owner is not player:
                player.money -= property.rent
            else:
                print(f"\nYou've landed on a property. {property}")
                choice = input("Would you like to buy this property? \n")
                while choice not in self.propertyChoices:
                    print("\nInvalid choice...")
                    choice = input("Would you like to buy this property? \n")

                if player.money <= property.price:
                    print("You don't have enough money...")
                    return

                if choice == "y":
                    player.money -= property.price
                    property.owner = player
                    player.properties.append(property)
                elif choice == "n":
                    return

        else:
            return


class Player:
    def __init__(self, name):
        self.name = name
        self.money = 1500
        self.location = 0
        self.properties = []
        self.inJail = False

    def roll(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        diceRoll = dice1 + dice2
        print(f"You rolled... Dice 1: {dice1}, Dice 2: {dice2}, Total: {diceRoll}")
        currTile = (self.location + diceRoll) % 40
        if self.inJail:
            return dice1, dice2, currTile

        self.location = currTile
        print(f"Your current tile: {currTile+1}\n")

        return dice1, dice2, currTile

    def turn(self, doubles=0):
        if doubles == 3:
            self.location = 8
            self.inJail = True
            return

        if self.inJail:
            choices = {"pay", "roll", "stay"}
            choice = input(
                "\nYou're in jail. Pay $50, try to roll doubles, or stay in jail?\n"
                "Choices: {pay, roll, stay}\n"
            )
            while choice not in choices:
                print("\nThat is not a valid option")
                choice = input(
                    "You're in jail. Pay $50, try to roll doubles, or stay in jail?\n"
                    "Choices: {pay, roll, stay}\n"
                )
            if choice == "pay":
                self.money -= 50
                print(f"{self.name} balance is now: ${self.money}")
                self.inJail = False
                return
            elif choice == "roll":
                dice1, dice2, _ = self.roll()
                if dice1 == dice2:
                    self.inJail = False
                return
            elif choice == "stay":
                return

        self.doubles = doubles
        print(
            f"It's your turn {self.name}!\n"
            f"Balance: {self.money}\n"
            f"Current Tile: {self.location}\n"
            f"Properties: {self.properties}\n"
        )
        roll_prompt = input("Press r to roll!\n")
        while roll_prompt != "r":
            print("\nInvalid input!!!")
            roll_prompt = input("Press r to roll!\n")

        dice1, dice2, currTile = self.roll()
        board.handleProperty(self)

        if currTile == 8:
            self.inJail = True

        if dice1 == dice2:
            self.turn(self.doubles + 1)


class Property:
    def __init__(self, location: int, price: int, rent: int):
        self.price = price
        self.rent = rent
        self.location = location
        self.owner = None

    def __repr__(self):
        return (
            f"Property @ Tile {self.location}"
            f"(Price: ${self.price}, Rent: ${self.rent})"
        )


board = Board()
p1 = Player("Alan")
while p1.money > 0:
    p1.turn(0)
