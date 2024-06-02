import random


class Board:
    def __init__(self):
        self.board = dict()
        self.propertyChoices = {"y", "n"}
        for i in range(40):
            self.board[i] = None

        self.board[3] = Property(3, 200, 50)
        self.board[7] = Property(7, 300, 75)
        self.board[13] = Property(13, 350, 110)
        self.board[19] = Property(19, 400, 150)
        self.board[23] = Property(23, 500, 170)
        self.board[31] = Property(31, 700, 300)
        self.board[35] = Property(35, 800, 400)
        self.board[27] = Property(27, 550, 250)
        self.board[15] = Property(15, 400, 150)
        self.board[29] = Property(29, 600, 290)
        self.board[38] = Property(38, 100, 600)

    def handleProperty(self, player):
        currTile = player.location
        if self.board[currTile] is not None:
            property = self.board[currTile]
            if property.owner:
                if property.owner is not player:
                    print(
                        f"{player.name}, you've landed on {property.owner.name}'s property!\n"
                        f"You owe them ${property.rent}..."
                    )
                    input("Press any button to continue...")
                    player.money -= property.rent
                    property.owner.money += property.rent
                    return
                else:
                    return
            else:
                print(f"\nYou've landed on a property. {property}")
                choice = input(
                    "Would you like to buy this property? \n" "Choices: {y, n}"
                )
                while choice not in self.propertyChoices:
                    print("\nInvalid choice...")
                    choice = input(
                        "Would you like to buy this property? \n" "Choices: {y, n}"
                    )

                if choice == "y":
                    if player.money <= property.price:
                        print("You don't have enough money...")
                        input("Press any button to continue...")
                        return
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
        print(f"\nYou rolled... Dice 1: {dice1}, Dice 2: {dice2}, Total: {diceRoll}")
        currTile = (self.location + diceRoll) % 40
        if self.inJail:
            return dice1, dice2, currTile

        self.location = currTile
        print(f"Your current tile: {currTile+1}\n")

        return dice1, dice2, currTile

    def turn(self, doubles=0):
        print(
            f"\nIt's your turn {self.name}!\n"
            f"Balance: ${self.money}\n"
            f"Current Tile: {self.location+1}\n"
            f"Properties: {self.properties}\n"
        )

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
                if self.money > 50:
                    self.money -= 50
                    print("You're now out of jail!")
                    print(f"{self.name}'s balance is now: ${self.money}")
                    self.inJail = False
                    return
                else:
                    print("You don't have enough money...")
                    input("Press any button to continue...")
                    return

            elif choice == "roll":
                dice1, dice2, _ = self.roll()
                if dice1 == dice2:
                    self.inJail = False
                    print("You rolled doubles... You're free!")
                    return

                print("You did not roll doubles... You stay in jail.")
                return
            elif choice == "stay":
                return

        self.doubles = doubles

        roll_prompt = input("Press r to roll! ")
        while roll_prompt != "r":
            print("\nInvalid input!!!")
            roll_prompt = input("Press r to roll!\n")

        dice1, dice2, currTile = self.roll()
        board.handleProperty(self)

        if self.money <= 0:
            return

        if currTile == 20:
            self.inJail = True

        if dice1 == dice2:
            print("You rolled doubles! Roll again!")
            self.turn(self.doubles + 1)


class Property:
    def __init__(self, location: int, price: int, rent: int):
        self.price = price
        self.rent = rent
        self.location = location
        self.owner = None

    def __repr__(self):
        return (
            f"Property @ Tile {self.location+1}"
            f"(Price: ${self.price}, Rent: ${self.rent})"
        )


board = Board()
p1 = Player("Alan")
p2 = Player("Melissa")
players = [p1, p2]

while players and len(players) > 1:
    for player in players:
        player.turn()
        if player.money <= 0:
            players.remove(player)
            print(f"{player.name} is out of money and has lost!")

print("The winner is:", players[0].name)
