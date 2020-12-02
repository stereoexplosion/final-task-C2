import random
import copy

miss_cell = "T"
damage_cell ="X"
aura_cell = "*"
destroyed_cell = "W"
ship_cell = "A"
empty_cell = "O"

size = 6

ships_list = [[1, 3], [2, 2], [3, 1]]

class Board(object):
    def __init__(self):
        self.board = []
        self.spawned = []

    def create(self):
        for row in range(size):
            self.board.append([empty_cell] * size)

    def random_arrangement_ship(self):

        for ship in ships_list:
            for unit in range(ship[0]):

                spawning = True
                while spawning:

                    global randship
                    randship = random.randrange(2)
                    if randship == 0:
                        location_y = random.randrange(size)
                        location_x = random.randrange(size - (ship[1] - 1))
                    else:
                        location_y = random.randrange(size - (ship[1] - 1))
                        location_x = random.randrange(size)

                    offset = 0
                    for testing in range(ship[1]):
                        if randship == 0 and self.board[location_y][location_x + offset] != empty_cell:
                            continue
                        elif randship == 1 and self.board[location_y + offset][location_x] != empty_cell:
                            continue
                        offset += 1
                        if offset == ship[1]:
                            spawning = False

                offset = 0
                current_ship = []
                for marker in range(ship[1]):
                    if randship == 0:
                        self.board[location_y][location_x + offset] = ship_cell
                        current_ship.append([location_y, location_x + offset])
                    else:
                        self.board[location_y + offset][location_x] = ship_cell
                        current_ship.append([location_y + offset, location_x])
                    offset += 1
                self.spawned.append(current_ship)

                for unit_point in current_ship:
                    for buffer_point in ([0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                        b_point_y = unit_point[0] + buffer_point[0]
                        b_point_x = unit_point[1] + buffer_point[1]
                        if b_point_y in range(size) and b_point_x in range(size):
                            if self.board[b_point_y][b_point_x] == empty_cell:
                                self.board[b_point_y][b_point_x] = aura_cell

    def updating(self, ship):
        for unit in ship:
            for buffer_point in ([0, 0], [0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]):
                b_point_y = unit[0] + buffer_point[0]
                b_point_x = unit[1] + buffer_point[1]
                if b_point_y in range(size) and b_point_x in range(size):
                    if self.board[b_point_y][b_point_x] == aura_cell:
                        self.board[b_point_y][b_point_x] = miss_cell
                    elif self.board[b_point_y][b_point_x] == damage_cell:
                        self.board[b_point_y][b_point_x] = destroyed_cell

    def state_of_ships(enemy):
        global destroy
        destroy = False
        for d_ship in enemy.spawned:
            damage = 0
            for d_unit in d_ship:
                if enemy.board[d_unit[0]][d_unit[1]] == damage_cell:
                    damage += 1
            if damage == len(d_ship):
                enemy.updating(d_ship)
                enemy.spawned.remove(d_ship)
                destroy = True

    @staticmethod
    def mirror_bot():
        stealth_bot.board = copy.deepcopy(bot.board)
        for i in range(size):
            for j in range(size):
                if stealth_bot.board[i][j] == aura_cell or stealth_bot.board[i][j] == ship_cell:
                    stealth_bot.board[i][j] = empty_cell
        return stealth_bot.board

class Game(object):
    @staticmethod
    def print_boards():
        print("\n    Ваше поле" + (" " * (size + 2)) + "Поле противника")
        print("    " + (" ".join(str(i) for i in list(range(size)))), end=(" " * 2))
        print("    " + (" ".join(str(i) for i in list(range(size)))))
        print("   " + (" |" * size), end=(" " * 2))
        print("   " + (" |" * size))
        n = 0
        monitoring = True
        for i in range(size):
            if monitoring:
                print(str(n) + " - " + "|".join(str(i) for i in player.board[n]), end=(" " * 2))
                print(str(n) + " - " + "|".join(str(i) for i in stealth_bot.board[n]))
            else:
                print(str(n) + " - " + "|".join(str(i) for i in player.board[n]).replace(aura_cell, empty_cell), end=(" " * 2))
                print(str(n) + " - " + "|".join(str(i) for i in stealth_bot.board[n]).replace(ship_cell, empty_cell).replace(aura_cell, empty_cell))
            n += 1

    @staticmethod
    def bot_pass():
        bot_guessing = True
        while bot_guessing:

            if len(player.spawned) == 0:
                break

            bot_intuition = random.randrange(size * 6)

            if bot_intuition == 0:
                bot_int_ship = random.randrange(len(player.spawned))
                bot_int_unit = random.randrange(len(player.spawned[bot_int_ship]))
                bot_guess_y = player.spawned[bot_int_ship][bot_int_unit][0]
                bot_guess_x = player.spawned[bot_int_ship][bot_int_unit][1]

            else:
                bot_guess_y = random.randrange(size)
                bot_guess_x = random.randrange(size)

            if player.board[bot_guess_y][bot_guess_x] == ship_cell:
                player.board[bot_guess_y][bot_guess_x] = damage_cell
                Board.state_of_ships(player)
                if destroy:
                    print("\nБот уничтожил ваш корабль!")
                else:
                    print("\nБот повредил ваш корабль!")

            elif player.board[bot_guess_y][bot_guess_x] == empty_cell or player.board[bot_guess_y][bot_guess_x] == aura_cell:
                player.board[bot_guess_y][bot_guess_x] = miss_cell
                print("\nБот выстрелил мимо!")
                break

            else:
                continue

print("\"Морской Бой\"\n")

bot = Board()
bot.create()
bot.random_arrangement_ship()

player = Board()
player.create()
player.random_arrangement_ship()

stealth_bot = Board()
stealth_bot.create()

game = True
while game:
    Game.print_boards()

    guessing = True
    while guessing:

        guess_x = input("Выберите столбец для стрельбы: ")
        guess_y = input("Выберите строку для стрельбы: ")

        if not guess_x.isdigit() or not guess_y.isdigit():
            print("\nВы ввели неверные координаты!")
            continue

        guess_x = int(guess_x)
        guess_y = int(guess_y)

        if not (guess_x in range(size)) or not (guess_y in range(size)):
            print("\nНе хватает дальности орудий! Пожалуйста, стреляйте по клеткам поля боя :)")
            continue

        elif bot.board[guess_y][guess_x] == ship_cell:
            bot.board[guess_y][guess_x] = damage_cell
            Board.state_of_ships(bot)
            if destroy:
                print("\nВы уничтожили корабль противника!", end=" ")
                Board.mirror_bot()
            else:
                print("\nВы повредили корабль противника!", end=" ")
                Board.mirror_bot()
            break

        elif bot.board[guess_y][guess_x] == empty_cell or bot.board[guess_y][guess_x] == aura_cell:
            bot.board[guess_y][guess_x] = miss_cell
            print("\nВы промахнулись!", end=" ")
            Board.mirror_bot()
            Game.bot_pass()

        else:
            print("\nВы уже выстрелили в этот квадрат! Пожалуйста, выберите другой")
            continue
        break

    if len(bot.spawned) == 0:
        input("Вы разгромили противника!")
        break

    if len(player.spawned) == 0:
        print("Машинный разум потопил все ваши суда! :(")
        input("Судна оставшиеся у противника: " + str(len(bot.spawned)) + ".")
        break