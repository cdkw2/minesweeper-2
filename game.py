import random

def create_board(size, num_mines):
    board = [[0 for _ in range(size)] for _ in range(size)]
    mines = set()
    while len(mines) < num_mines:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if (x, y) not in mines:
            board[x][y] = "M"
            mines.add((x, y))
    return board

def count_adjacent_mines(board, x, y):
    count = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            xi, yi = x + dx, y + dy
            if 0 <= xi < len(board) and 0 <= yi < len(board) and board[xi][yi] == "M":
                count += 1
    return count

def reveal_cells(board, x, y):
    if board[x][y] == "M":
        return [(x, y, "M")]

    revealed = [(x, y, count_adjacent_mines(board, x, y))]
    if revealed[0][2] == 0:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                xi, yi = x + dx, y + dy
                if 0 <= xi < len(board) and 0 <= yi < len(board) and board[xi][yi] != "M":
                    revealed.extend(reveal_cells(board, xi, yi))

    return list(set(revealed))

def play_game():
    size = 8
    num_mines = 10
    board = create_board(size, num_mines)
    hidden_board = [["#" for _ in range(size)] for _ in range(size)]
    flags = set()
    revealed_cells = set()

    while True:
        print_board(hidden_board)
        action = input("Enter action (R for reveal, F for flag) and coordinates (x, y): ").split()
        if len(action) != 3 or action[0] not in ["R", "F"] or not action[1].isdigit() or not action[2].isdigit():
            print("Invalid input. Please try again.")
            continue

        x, y = int(action[1]), int(action[2])
        if action[0] == "R":
            if (x, y) in flags:
                print("Cell is flagged. Unflag it before revealing.")
                continue
            revealed = reveal_cells(board, x, y)
            if revealed[0][2] == "M":
                print("You hit a mine! Game over.")
                break

            for xi, yi, value in revealed:
                hidden_board[xi][yi] = str(value)
                revealed_cells.add((xi, yi))

            if len(revealed_cells) == size * size - num_mines:
                print_board(hidden_board)
                print("Congratulations! You won!")
                break
        elif action[0] == "F":
            if (x, y) in flags:
                hidden_board[x][y] = "#"
                flags.remove((x, y))
            else:
                hidden_board[x][y] = "F"
                flags.add((x, y))

def print_board(board):
    print("\n".join(" ".join(row) for row in board))
    print()

if __name__ == "__main__":
    play_game()
