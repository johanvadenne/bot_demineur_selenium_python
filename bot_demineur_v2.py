import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import keyboard
import pprint
import time
import random

def main():
    try:
        bot = Bot()
        
        bot.init_cellule()
        bot.calcul_proba_mine()
        bot.affiche_proba()


        keyboard.wait("enter")
    except:
        keyboard.wait("enter")
        



dict_img_demineur = {
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
        self.cellules = []
        self.demineur_board_html = ""

        # initialisation du navigateur
        self.driver = webdriver.Chrome()
        self.action = ActionChains(self.driver)
        self.page_content = self.driver.get(self.url)

        self.driver.find_element(By.CLASS_NAME, "css-k8o10q").click()

        # attendre que la touche "entrée" soit pressée
        keyboard.wait("enter")
        
        self.init_board_demineur()
    
    def init_board_demineur(self):
        # récupère le tableau
        self.demineur_board_html = self.driver.find_element(By.ID,"board")
        # récupère les cellule
        cellules_html = self.demineur_board_html.find_elements(By.TAG_NAME, "img")
        
        self.calcul_size_board(self.demineur_board_html, cellules_html[0])
        self.init_cellule(cellules_html)
        self.random_click_start()
        
        
    
    def calcul_size_board(self, demineur_board_html, cellule_html) -> None:
        size = demineur_board_html.size
        width_board, height_board = size['width'], size['height']

        size = cellule_html.size
        width_cell, height_cell = size['width'], size['height']

        self.width = int(width_board/width_cell)
        self.height = int(height_board/height_cell)
        
    
    def init_cellule(self) -> None:
        
        cellules_html = self.demineur_board_html.find_elements(By.TAG_NAME, "img")
        
        x = 0
        y = 0
        nbr_ordre = 0
        self.cellules = []
        for cellule in cellules_html:
            new_cellule = Cellule(cellule, cellule.get_attribute("src"), x, y, nbr_ordre, self.action)
            self.cellules.append(new_cellule)
            
            y+=1
            nbr_ordre+=1
            if y >= self.width:
                y=0
                x+=1
            
        
    def random_click_start(self) -> None:
        self.cellules[random.randint(0, len(self.cellules)-1)].click()
    
    
    def calcul_proba_mine(self):
        for cellule in self.cellules:
            print(cellule.valeur)
            if isinstance(cellule.valeur, int):
                cellules_neighbours = self.get_cellules_neighbours(cellule.x, cellule.y)
                
                nbr_inconnu = 0
                for cellule_neighbour in cellules_neighbours:
                    if cellule_neighbour.valeur == '?':
                        nbr_inconnu+=1
                
                for cellule_neighbour in cellules_neighbours:
                    if cellule_neighbour.valeur == '?':
                        if nbr_inconnu > 0:
                            self.tab_probat.append(100/(nbr_inconnu-cellule.valeur))
                        else:
                            self.tab_probat.append(0)
    
    
    def affiche_proba(self):
        
        x = 0
        ligne = []
        for cellule in self.cellules:
            if x != cellule.x:
                print(ligne)
                ligne = [cellule.tab_probat]
            else:
                ligne.append(cellule.tab_probat)
        print(ligne)
                
            
    
    # def frop_flag(self):
        
    #     for cellule in self.cellules:
    #         if cellule.valeur == '?':
                
    #             if max(cellule.tab_probat) == 100:
    #                 cellule.drop_flag()
                
    #             if 
            
                            
                
                    
                
    def position_cell(self, x, y) -> int:
        return (x*self.width + y)
    
    
    def get_cellules_neighbours(self, i, j) -> list:
        # renvoie les voisins de la case (i, j)
        cellules_neighbours = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x, y) != (0, 0) and 0 <= i + x < self.height and 0 <= j + y < self.width:
                    cellules_neighbours.append(self.cellules[self.position_cell(i + x, j + y)])
        return cellules_neighbours


class Cellule:
    
    def __init__(self, img, src, x, y, nbr_ordre, action) -> None:
        self.img = img
        self.src = src
        self.x = x
        self.y = y
        self.nbr_ordre = nbr_ordre
        self.action = action
        self.valeur = dict_img_demineur[src]
        self.tab_probat = []
    
    def click(self) -> None:
        self.img.click()
    
    def drop_flag(self) -> None:
        self.action.context_click(self.img).perform()
    
    


if __name__ == "__main__":
    main()
