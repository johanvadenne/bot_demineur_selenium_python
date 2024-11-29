import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import keyboard
import pprint
import time

def main():
    try:
        bot = Bot()
        bot.show_grid()

        keyboard.wait("enter")
        
        for i in range(100):
            analyse = True
            while analyse:
                bot.init_board()
                grid_probat = bot.calcul_probat()
                analyse = bot.pose_drapeau(grid_probat)

            bot.init_board()
            grid_probat = bot.calcul_probat()
            bot.decouvre_case(grid_probat)


        keyboard.wait("enter")
    except:
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
        self.action = ActionChains(self.driver)




        self.get_page_content()

        # attendre que la touche "entrée" soit pressée
        # keyboard.wait("enter")


        self.init_tableau_demineur_html()

        # clique sur le bouton "accepter"
        self.driver.find_element(By.CLASS_NAME, "css-k8o10q").click()

        # clique sur le la case (0, 0)
        self.tab_cell_demineur_html[-1].click()

        self.calcul_size_board()
        
        # initialisation de la grille
        self.make_grid(self.width, self.height)



    def init_board(self):
        self.calcul_size_board()
        # initialisation de la grille
        self.make_grid(self.width, self.height)
        

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
            cases.append(dict[src])
        
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
        grid_probat = grid_probat = [[1 for _ in range(self.width)] for _ in range(self.height)]

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
                    nbr_cellule_inconnu=0
                    nbr_cellule_drapeau=0
                    for neighbour_x_y_cellule_conjoint in neighbours_cellule:
                        x_conjoint, y_conjoint = neighbour_x_y_cellule_conjoint

                        # récupère la valeur
                        valeur_conjoint = self.grid[x_conjoint][y_conjoint]

                        # vérifie si c'est un entier
                        if valeur_conjoint == '?':
                            nbr_cellule_inconnu+=1
                        if valeur_conjoint == '🚩':
                            nbr_cellule_drapeau+=1
                    
                    for neighbour_x_y_cellule_conjoint in neighbours_cellule:
                        x_conjoint, y_conjoint = neighbour_x_y_cellule_conjoint

                        # récupère la valeur
                        valeur_conjoint = self.grid[x_conjoint][y_conjoint]

                        # vérifie si c'est un entier
                        if valeur_conjoint == '?':
                            if valeur_cell-nbr_cellule_drapeau == 1:
                                grid_probat[x_conjoint][y_conjoint] == 999999999999
                            if nbr_cellule_inconnu != 0 and valeur_cell-nbr_cellule_drapeau > 0:
                                grid_probat[x_conjoint][y_conjoint] *= int(100/nbr_cellule_inconnu)
                            elif valeur_cell-nbr_cellule_drapeau == 0:
                                grid_probat[x_conjoint][y_conjoint] = -1
                            else:
                                grid_probat[x_conjoint][y_conjoint] = 0
                
                        if valeur_conjoint == 0 or valeur_conjoint == '🚩':
                            grid_probat[x_conjoint][y_conjoint] = 0
        
        for x in range(len(grid_probat)):
            for y in range(len(grid_probat[x])):
                if grid_probat[x][y] == 1:
                    grid_probat[x][y] = 0

        
        print(grid_probat)
                            
        return grid_probat
    
    def pose_drapeau(self, grid_probat):
        
        meilleur_probat = 0
        click_x = -1
        click_y = -1
        tab_meilleur_neighbours = [0]
        
        
        x=-1
        for line in self.grid:
            x+=1
            y=-1

            # parcour les cellule
            for cell in line:
                y+=1

                valeur_cell = self.grid[x][y]

                # si la cellule n'est pas trouvé
                if isinstance(valeur_cell, int):

                    # on récupère les bloc autour
                    neighbours = self.get_neighbours(x,y)
                    
                    meilleur_neighbour = -1
                    for neighbour_x_y in neighbours:
                        n_x = neighbour_x_y[0]
                        n_y = neighbour_x_y[1]
                        
                        if grid_probat[n_x][n_y] >= 999999999999:
                            position_element = n_x*self.width + n_y
                            self.action.context_click(self.tab_cell_demineur_html[position_element]).perform()
                            return True
                            
                        
                        if grid_probat[n_x][n_y] == meilleur_neighbour:
                            meilleur_neighbour = 0
                            temp_click_x = -1
                            temp_click_y = -1
                            break
                        
                        if grid_probat[n_x][n_y] > meilleur_neighbour:
                            meilleur_neighbour = grid_probat[n_x][n_y]
                            temp_click_x = n_x
                            temp_click_y = n_y
                    
                    if temp_click_x > -1 and temp_click_y > -1 and meilleur_neighbour > max(tab_meilleur_neighbours):
                        click_x = temp_click_x
                        click_y = temp_click_y
                    tab_meilleur_neighbours.append(meilleur_neighbour)
                    
        
        if max(tab_meilleur_neighbours) > 0:
            position_element = click_x*self.width + click_y
            self.action.context_click(self.tab_cell_demineur_html[position_element]).perform()
            return True
        else:
            return False
        
        
    def decouvre_case(self, grid_probat):
        
        x=-1
        for line in grid_probat:
            x+=1
            y=-1

            # parcour les cellule
            for cell in line:
                y+=1
                
                if cell < 0:
                    self.tab_cell_demineur_html[x*self.width+y].click()
                    
        




if __name__ == "__main__":
    main()
