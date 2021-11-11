def player_names():
    names.append(input("Podaj nazwę gracza, który będzie grał krzyżykami: "))
    names.append(input("Podaj nazwę gracza, który będzie grał kółkami: "))

def set_board_size():
    try:
        size = input("Podaj rozmiar planszy (wpisz liczbę z zakresu 3 - 15, np. 3 - plansza 3x3): ")
        if (size==''): return 3 # jeśli gracz nie wpisze żadnej wartości, wysyłana jest wartość domyślna - 3
        size = int(size)
        if (size<3 or size>15):
            print("\nNieprawidłowy zakres. Podaj liczbę z przedziału 3 - 15.")
            raise TypeError # podniesienie błędu w celu ponownego uruchomenia funkcji
        return size
    except TypeError:
        return set_board_size()
    except ValueError: # błąd ten podniesie się, kiedy gracz nie wpiszę poprawnej liczby
        print("\nPodaj liczbę!")
        return set_board_size()


def board(index):
    for i in range(1, board_size**2+1):
        if not i%board_size:
            print(f" {index[i]}") # brak pionowej kreski po wartości ze słownika board_index, ponieważ jest to ostatnie pole w rzędzie
            if i == board_size**2: break # wpisywana jest ostatnia wartość ze słownika board_index, break wstrzymuje narysowanie kolejnej poziomej linii
            print("---" + ("|---" * (board_size-1))) # rysowanie rozdzielających poziomych linii na planszy
            continue
        print(f" {index[i]} |", end="") # rysowanie rzędów, pionowa kreska w celu oddzielenia pól planszy

def player_move(p):
    try:
        move = int(input(f"{names[p]}, podaj numer miejsca, gdzie umieścić {signs[p]}: "))
        if move not in range(1, board_size**2+1): raise ValueError
    except ValueError: # błąd jest podnoszony jeśli gracz przekroczy zakres planszy, lub nie wpisze liczby
        print(f"Wpisz prawidłową liczbę z zakresu 1-{board_size**2}!")
        return player_move(p)
    if move in used_places: # sprawdzenie, czy wpisana liczba znajduje się na liśćie użytych pól
        print("To miejsce jest już zajęte!")
        return player_move(p)
    used_places.append(move) # dopisanie wpisanej liczby do listy użytych pól
    board_index[move] = signs[p] # wstawienie wartości do słownika board_index

def another_game():
    another = input("Czy chcesz zagrać jeszcze raz? (t/n) ")
    another.lower()
    return game() if another=='t' else quit() if another=='n' else another_game()

def winner():
    set_values = list(board_index.values()) # utworzenie listy ze wszystkich dotychczas zapisanych 'X', 'O', lub spacji
    # każda linia z podanego zakresu zostaje przekonwertowana w set - jeśli w linii znajdują się te same wartości, w secie znajdzie się tylko jedna wartość
    line_x1 = set(set_values[0::board_size+1]) # przekątna rysowana w dół
    line_x2 = set(set_values[-(board_size):0:-(board_size-1)]) # przekątna rysowana w górę
    for i in range(board_size):
        line_h = set(set_values[board_size * i: (i+1) * board_size]) # linie poziome
        line_v = set(set_values[i::board_size]) # linie pionowe
        lines = [line_h, line_v, line_x1, line_x2] # lista setów
        for j in range(4):
            if (lines[j] == {signs[which_move]}): # jeśli w lines znajduje się set z jedną wartością i będzie to znak używany przez aktualnego gracza, oznacza to, że zapełnił daną linię i zwyciężył
                print(f"\n{names[which_move]} zwycięża! Gratulacje!")
                return another_game()

############

def game():
    # zmienne ustawione jako globalne, tak by każda funkcja mogła się do nich odwoływać
    global names, signs, board_size, board_index, which_move, used_places
    names = []
    signs = ['X', 'O']
    board_size = set_board_size() # ustawienie rozmiaru planszy (domyślnie: 3x3)
    board_index = {i: " " for i in range(1, board_size**2+1)} # ustawienie pustego miejsca w każdym polu planszy gry
    which_move = 0
    used_places = [] # lista sprawdzająca, które pola planszy są już wykorzystane


    player_names() # zapisanie imion graczy
    board(board_index) # rysowanie planszy
    while (" " in board_index.values()): # jeśli żaden z graczy nie wygra, gra toczy się do momentu zapełnienia wszystkich pól
        print("\n")
        player_move(which_move)
        print("\n")
        board(board_index) # ponowne narysowanie planszy z uzupełnionymi polami
        winner() # sprawdzenie, czy w linii poziomej, pionowej lub przekątnej nie ma takich samych znaków, jeśli tak gra się kończy
        which_move = not which_move # odwrócenie indeksu, jeśli używane są names[0] i signs[0], to po odwróceniu przy następnej iteracji będą to names[1] i signs[1] i na odwrót
    print("Remis!")
    another_game() # funkcja uruchamiająca grę od nowa, lub wyłączająca program

###########

# Główna funkcja
game()