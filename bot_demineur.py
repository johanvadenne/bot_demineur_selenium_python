import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import keyboard
import pprint
import time

def main():
    bot = Bot()
    bot.show_grid()

    keyboard.wait("enter")



dict = {
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb3///97e3uVBMaVAAAAHklEQVQI12MIDQ0NARFBDAEMDFzkEl6rVq1i0AISAIlSC03msuDYAAAAAElFTkSuQmCC': '?',
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEW9vb17e3tXxGy+AAAAEElEQVQI12P4/5+hgYF4BAAJYgl/JfpRmAAAAABJRU5ErkJggg==' : 0,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AAP97e3u7pKrVAAAAJUlEQVQI12NYBQQMDQxAACUCgAQjiGAFEaIQLiYhGgojEHqBGAB4Gw2cMF3q+AAAAABJRU5ErkJggg==' : 1,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AewB7e3vro336AAAANUlEQVQI12NYBQQMDQxAACFCQxkYGkNDHRgaA1gdgGJgIhQowRoCknUAygIZYCVgAqwNQQAA1rsQB7h1rwIAAAAASUVORK5CYII=' : 2,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb3/AAB7e3uBZQfoAAAAKUlEQVQI12NYBQQMDQxAACYaQ0PBhAOQywojWIFiIAIhBlICJiDaEAQAtlYPHU2zahQAAAAASUVORK5CYII=' : 3,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0AAHt7e3vZn4u5AAAAJklEQVQI12NYBQQMDQxAACFERWFECIxoDA11ABNAJUAuBsGARAAAgHoNeXfAhZYAAAAASUVORK5CYII=' : 4,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb17AAB7e3sERFEmAAAAKUlEQVQI12NYBQQMDQxAACYaQ0MdoEQAiBsAEYNIAJWwQgi4Oog2BAEA7gEQV+EiCoQAAAAASUVORK5CYII=': 5,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAgMAAABinRfyAAAACVBMVEW9vb0Ae3t7e3tXnVpnAAAAKklEQVQI12NYBQQMDQxAACFCQxkYGsFEAAOMgIo5ALmsEALMBSmGaEMQAOO9EHd34ZsRAAAAAElFTkSuQmCC': 6,
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAAD1BMVEW9vb3///97e3sAAAD/AABQHuKJAAAAOklEQVQI12MQhAABGIOJQZABDJRADBYHCIPFBcpwcUGIIKsB6zJAZxgbQxjGQIDEQFghoAQBDExQBgCHngoRLPdU8QAAAABJRU5ErkJggg==': '🚩'
    }



class Bot:

    def __init__(self):
        self.url = "https://xn--dmineur-bya.eu/"


        # liste des cases du démineur
        self.tab_cell_demineur_html = []

        # taille de la grille (nombre de cases)
        self.width = 0
        self.height = 0


        # initialisation du navigateur
        self.driver = webdriver.Chrome()




        self.get_page_content()

        # attendre que la touche "entrée" soit pressée
        # keyboard.wait("enter")


        self.init_tableau_demineur_html()

        # clique sur le bouton "accepter"
        self.driver.find_element(By.CLASS_NAME, "css-k8o10q").click()

        # clique sur le la case (0, 0)
        self.tab_cell_demineur_html[0].click()

        # clique droit sur la case (0, 0)




        start_time = time.time()
        # calcul de la taille du tableau
        self.calcul_size_board()
        end_time = time.time()
        print(f"Temps d'exécution calcul_size_board() : {end_time - start_time:.5f} secondes")

        start_time = time.time()
        # initialisation de la grille
        self.make_grid(self.width, self.height)
        end_time = time.time()
        print(f"Temps d'exécution make_grid() : {end_time - start_time:.5f} secondes")

        start_time = time.time()
        self.calcul_probat()
        end_time = time.time()
        print(f"Temps d'exécution calcul_probat() : {end_time - start_time:.5f} secondes")





    def get_page_content(self):
        self.page_content = self.driver.get(self.url)


    def init_tableau_demineur_html(self):
        self.table_demineur_html = self.driver.find_element(By.ID,"board")
        self.tab_cell_demineur_html = self.table_demineur_html.find_elements(By.TAG_NAME, "img")


    def calcul_size_board(self) :
        size = self.table_demineur_html.size
        width_board, height_board = size['width'], size['height']

        size = self.tab_cell_demineur_html[0].size
        width_cell, height_cell = size['width'], size['height']

        self.width = int(width_board/width_cell)
        self.height = int(height_board/height_cell)

    def cases_html_to_char(self, cases_html):
        # Crée un cache pour les valeurs déjà récupérées
        src_cache = {}
        cases = []
        for case in cases_html:
            src = case.get_attribute("src")
            if src not in src_cache:
                src_cache[src] = dict[src]  # Cache le résultat
            cases.append(src_cache[src])
        return cases





    def make_grid(self, width, height):

        start_time = time.time()
        temp = self.cases_html_to_char(self.tab_cell_demineur_html)
        end_time = time.time()
        print(f"Temps d'exécution cases_html_to_char() : {end_time - start_time:.5f} secondes")


        grid = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(temp.pop(0))
            grid.append(row)
        self.grid = grid




    def show_grid(self):
        # affiche la grille dans la console
        for row in self.grid:
            for cell in row:
                print(cell, end='  ')
            print("")



    def get_neighbours(self, i, j):
        # renvoie les voisins de la case (i, j)
        neighbours = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0) and 0 <= i + x < self.height and 0 <= j + y < self.width:
                    neighbours.append((i + x, j + y))
        return neighbours

    def check_case(self, i, j):
        # Renvoie True si la condition de la case (i, j) est vérifiée
        case_val = self.grid[i][j]  # La valeur de la case (i, j)

        # Si la case contient un '?' (case non révélée), elle ne peut pas être vérifiée
        if case_val == '?':
            return False

        # Obtient les voisins de la case (i, j)
        neighbours = self.get_neighbours(i, j)

        # Compte le nombre de drapeaux ('🚩') autour de la case (i, j)
        flags_count = sum(1 for x, y in neighbours if self.grid[x][y] == '🚩')

        # Si la valeur de la case correspond au nombre de drapeaux autour d'elle, retourne True
        if case_val == flags_count:
            return True
        return False




    def calcul_probat(self):

        # créer un nouveai u tableau vide avec une valeur de 1 par défaut
        grid_test = grid_test = [[1 for _ in range(self.width)] for _ in range(self.height)]

        # parcours les ligne du tableau
        x_cell=-1
        for line in self.grid:
            x_cell+=1
            y_cell=-1

            # parcour les cellule
            for cell in line:
                y_cell+=1

                valeur_cell = self.grid[x_cell][y_cell]

                # si la cellule n'est pas trouvé
                if isinstance(valeur_cell, int):

                    # on récupère les bloc autour
                    neighbours_cellule = self.get_neighbours(x_cell,y_cell)
                    for neighbour_x_y_cellule_conjoint in neighbours_cellule:
                        x_conjoint, y_conjoint = neighbour_x_y_cellule_conjoint

                        # récupère la valeur
                        valeur_conjoint = self.grid[x_conjoint][y_conjoint]

                        nbr_cellule_inconnu=0

                        # vérifie si c'est un entier
                        if valeur_conjoint == '?':
                            nbr_cellule_inconnu+=1

                    if nbr_cellule_inconnu != 0:
                        grid_test[x_cell][y_cell] *= 100/nbr_cellule_inconnu
                    else:
                        grid_test[x_cell][y_cell] = 0


        pprint.pprint(grid_test)









if __name__ == "__main__":
    main()










# ?  ?  ?  ?  ?  ?  ?  ?  ?
# 0  1  ?  ?  ?  ?  ?  ?  ?
# 0  1  1  2  ?  ?  ?  ?  ?
# 0  0  0  1  ?  ?  ?  ?  ?
# 0  0  0  2  ?  ?  ?  ?  ?
# 0  0  0  1  ?  ?  ?  ?  ?
# 0  0  0  2  ?  ?  ?  ?  ?
# 0  0  0  1  ?  ?  ?  ?  ?
# 0  0  0  1  ?  ?  ?  ?  ?