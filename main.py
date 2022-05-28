import sys,pygame
from mode import *
from button import *
from constant import *

pygame.init()
pygame.display.set_caption("Tic-Tac-Toe")
ekran=pygame.display.set_mode((1280,720))

class Game():
    def __init__(self) -> None:
        self.home_menu()
    
    def home_menu(self):
        while True:
            ekran    =pygame.display.set_mode((1280,720))
            mousePos =pygame.mouse.get_pos()
            backG    =pygame.image.load("datas/background.jpg")
            ekran.blit(backG,(0,0))

            menuTxt  =self.getFont(90).render("NTP",True,"#EB212E")
            menuRect =menuTxt.get_rect(center=(640,175))
            ekran.blit(menuTxt,menuRect)

            self.multiB  =Button(image=None, pos=(640, 350), textInput="Multiplayer", font=self.getFont(50), baseColor="#d7fcd4", hoveringColor="White")
            self.compB   =Button(image=None, pos=(640, 450), textInput="Computer",    font=self.getFont(50), baseColor="#d7fcd4", hoveringColor="White")
            self.quitB   =Button(image=None, pos=(640, 550), textInput="Quit",        font=self.getFont(40), baseColor="#d7fcd4", hoveringColor="White")
            self.name    =Button(image=None, pos=(830, 205), textInput="by zaimj",    font=self.getFont(10), baseColor="white",   hoveringColor="White")

            ekran.blit(menuTxt,menuRect)

            for button in [self.multiB,self.compB,self.quitB,self.name]:
                button.hoverColor(mousePos)
                button.update(ekran)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if self.multiB.checkMouse(mousePos):
                        self.multiMode()
                    if self.compB.checkMouse(mousePos):
                        self.compMode()
                    if self.quitB.checkMouse(mousePos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def getFont(self,size):
        return pygame.font.Font("datas/font.ttf",size)

    def multiMode(self):
        MULTIGame()

    def compMode(self):
        while True:
            mousePos  =pygame.mouse.get_pos()
            
            ekran.fill(CREAM)
            DIFF       =self.getFont(45).render("CHOOSE THE DIFFICULTY",True,GOLDEN_BRWN)
            DIFF_RECT  =DIFF.get_rect(center=(600,200))
            ekran.blit(DIFF,DIFF_RECT)

            self.easyB   =Button(image=None, pos=(640, 350), textInput="Easy", font=self.getFont(40), baseColor=GOLDEN_BRWN, hoveringColor=WHISKEY_BRWN)
            self.hardB   =Button(image=None, pos=(640, 450), textInput="Hard", font=self.getFont(40), baseColor=GOLDEN_BRWN, hoveringColor=WHISKEY_BRWN)

            for button in [self.easyB,self.hardB]:
                button.hoverColor(mousePos)
                button.update(ekran)
            
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==pygame.MOUSEBUTTONDOWN:
                    if self.easyB.checkMouse(mousePos):
                        AIGame(diff="Easy")
                    elif self.hardB.checkMouse(mousePos):
                        AIGame(diff="Hard")
            
            pygame.display.update()


tictactoe=Game()