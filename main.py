import random


class Map:
    def __init__(self):
        self.map = {}
        for i in range(15):
            self.map[i] = None

        self.map[3] = Property(3, 200, 50)
        self.map[7] = Property(7, 400, 100)
        self.map[13] = Property(13, 800, 350)


class Player:
    def __init__(self, piece, gameMap):
        self.piece = piece
        self.money = 1500
        self.location = 0
        self.properties = []
        self.inJail = False
        self.gameMap = gameMap

    def turn(self, doubles):
        if doubles == 3:
            self.location = 8
            self.inJail = True
            return

        if self.inJail:
            choices = {"pay", "roll", "stay"}
            choice = input(
                "You're in jail. Pay $50, try to roll doubles, or stay in jail?\n"
            )
            while choice not in choices:
                print("That is not a valid option")
                choice = input(
                    "You're in jail. Pay $50, try to roll doubles, or stay in jail?\n"
                )
            if choice == "pay":
                self.money -= 50
                print(f"{self.piece} balance is now: ${self.money}")
                self.inJail = False
                return
            elif choice == "roll":
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                diceRoll = dice1 + dice2
                print(
                    "You rolled...",
                    "Dice 1:",
                    dice1,
                    "Dice 2:",
                    dice2,
                    "Total:",
                    diceRoll,
                )
                if dice1 == dice2:
                    self.inJail = False
                    return
                else:
                    return
            elif choice == "stay":
                return

        self.doubles = doubles
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        diceRoll = dice1 + dice2
        print("You rolled...", "Dice 1:", dice1, "Dice 2:", dice2, "Total:", diceRoll)
        currTile = (self.location + diceRoll) % 14
        self.location = currTile
        print("Your current tile:", currTile)

        if currTile == 8:
            self.inJail = True

        if self.gameMap.map[currTile] is not None:
            property = self.gameMap.map[currTile]
            if property.owner:
                self.money -= property.rent
                property.owner.money += property.rent
            else:
                choices = {"y", "n"}
                print(f"You've landed on a property. {property}")
                choice = input("Would you like to buy this property? \n")
                while choice not in choices:
                    print("Invalid choice...")
                    choice = input("Would you like to buy this property? \n")

                if choice == "y":
                    self.money -= property.price
                    property.owner = self
                    self.properties.append(property)

        if dice1 == dice2:
            self.turn(self.doubles + 1)


class Property:
    def __init__(self, location, price, rent):
        self.price = price
        self.rent = rent
        self.location = location
        self.owner = None

    def __repr__(self):
        return (
            f"Property @ Tile {self.location}"
            f"(Price: ${self.price}, Rent: ${self.rent})"
        )


board = Map()
p1 = Player("Alan", board)
print(board)
while board.map[p1.location] is None:
    p1.turn(0)
    print(p1.location, p1.money, list(p1.properties))

p1.turn(0)
