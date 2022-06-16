import copy,random,pygame,sys,numpy as np
from multipledispatch import dispatch
from abc import ABC,abstractmethod
from constant import *
from button import *

ekran=pygame.display.set_mode((1280,720))

class ModeFunction(ABC):
    @abstractmethod
    def drawGrid(self):
        pass

    @abstractmethod
    def drawSymbol(self):
        pass

    @abstractmethod
    def playerMove(self):
        pass

    @abstractmethod
    def nextTurn(self):
        pass

    @abstractmethod
    def gameOver(self):
        pass


class Grid:
    def __init__(self) -> None:
        self.grid       =np.zeros((ROWS,COLS))
        self.emptyGrids =self.grid
        self.filledGrid =0
    
    
    def winning(self,areyawinning=False):
        #vertical
        for col in range(COLS):
            if self.grid[0][col]==self.grid[1][col]==self.grid[2][col] != 0:
                if areyawinning:
                    color  = RED_WINE if self.grids[0][col]==2 else NAVY_BLUE
                    pos1   = (col*SQSIZE + SQSIZE//2, 20)
                    pos2   = (col*SQSIZE + SQSIZE//2, GRID_HEIGHT-20)
                    pygame.draw.line(ekran, color, pos1, pos2, LINE_WIDTH)
                return self.grid[0][col]

        #horizontal
        for row in range(ROWS):
            if self.grid[row][0]==self.grid[row][1]==self.grid[row][2] != 0:
                if areyawinning:
                    color  = RED_WINE if self.grid[row][0]==2 else NAVY_BLUE
                    pos1   = (20, row*SQSIZE + SQSIZE//2)
                    pos2   = (GRID_WIDTH-20, row*SQSIZE + SQSIZE//2)
                    pygame.draw.line(ekran, color, pos1, pos2, CROSS_WIDTH)
                return self.grid[row][0]
            
        # \
        if self.grid[0][0]==self.grid[1][1]==self.grid[2][2] != 0:
            if areyawinning:
                color  = RED_WINE if self.grid[1][1]==2 else NAVY_BLUE
                pos1   = (20,20)
                pos2   = (GRID_WIDTH-20, GRID_HEIGHT-20)
                pygame.draw.line(ekran, color, pos1, pos2, CROSS_WIDTH)
            return self.grid[1][1]
        
        # /
        if self.grid[2][0]==self.grid[1][1]==self.grid[0][2] != 0:
            if areyawinning:
                color  = RED_WINE if self.grid[1][1]==2 else NAVY_BLUE
                pos1   = (20, GRID_HEIGHT-20)
                pos2   = (GRID_WIDTH-20, 20)
                pygame.draw.line(ekran, color, pos1, pos2, CROSS_WIDTH)
            return self.grid[1][1]
        
        return 0
    
    def markedGrid(self,row,col,oyuncu):
        self.grid[row][col]=oyuncu
        self.filledGrid+=1
    
    def emptySquare(self,row,col):
        return self.grid[row][col]==0
    
    def getEmptySquare(self):
        newGrid=[]
        for row in range(ROWS):
            for col in range(COLS):
                if self.emptySquare(row,col):
                    newGrid.append((row,col))
        return newGrid
    
    def fullGrid(self):
        return self.filledGrid==9
    
    def emptyGrid(self):
        return self.filledGrid==0
    
    def resetGame(self):
        self.__init__()


class Mode(ModeFunction):
    def __init__(self,mode:str) -> None:
        self.gamegrid  =Grid()
        self.mode      =mode
        self.oyuncu    =1
        self.run       =True
        self.drawGrid()

    def drawGrid(self):
        ekran.fill(CHMPGNE_P)

        pygame.draw.line(ekran, MIDNIGHT_GRN, (SQSIZE,0),             (SQSIZE,GRID_HEIGHT),            LINE_WIDTH)
        pygame.draw.line(ekran, MIDNIGHT_GRN, (GRID_WIDTH-SQSIZE,0),  (GRID_WIDTH-SQSIZE,GRID_HEIGHT), LINE_WIDTH)

        pygame.draw.line(ekran, MIDNIGHT_GRN, (0,SQSIZE),             (GRID_WIDTH,SQSIZE),             LINE_WIDTH)
        pygame.draw.line(ekran, MIDNIGHT_GRN, (0,GRID_HEIGHT-SQSIZE), (GRID_WIDTH,GRID_HEIGHT-SQSIZE), LINE_WIDTH)

    def drawSymbol(self,row,col):
        if self.oyuncu==1:
            firstX1   =(col*SQSIZE + OFFSET,        row*SQSIZE + OFFSET)
            firstX2   =(col*SQSIZE + SQSIZE-OFFSET, row*SQSIZE + SQSIZE-OFFSET)

            secondX1  =(col*SQSIZE + OFFSET,        row*SQSIZE + SQSIZE-OFFSET)
            secondX2  =(col*SQSIZE + SQSIZE-OFFSET, row*SQSIZE + OFFSET)

            pygame.draw.line(ekran, NAVY_BLUE, firstX1,  firstX2,  CROSS_WIDTH)
            pygame.draw.line(ekran, NAVY_BLUE, secondX1, secondX2, CROSS_WIDTH)
        
        elif self.oyuncu==2:
            mid = (col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2)
            pygame.draw.circle(ekran, RED_WINE, mid, RADS, CIRCLE_WIDTH)
        
    
    def playerMove(self,row,col):
        self.gamegrid.markedGrid(row,col,self.oyuncu)
        self.drawSymbol(row,col)
        self.nextTurn()
    
    def nextTurn(self):
        self.oyuncu = self.oyuncu%2+1

    def gameOver(self):
        return self.gamegrid.winning(areyawinning=True) != 0 or self.gamegrid.fullGrid()
    
    def resetGame(self):
        self.__init__()

    @abstractmethod
    def gamePlay(self):
        pass


class MultiplayerMode(Mode):
    def __init__(self) -> None:
        super().__init__(mode='MULTI')
        self.gamePlay()
    
    def gamePlay(self):
        ekran =pygame.display.set_mode((1200,800))
        self.drawGrid()

        while True:
            multiG     =self.gamegrid
            mouse      =pygame.mouse.get_pos()
            multiTxt   =pygame.font.Font("datas/font.ttf",40).render("2 Players",True,MIDNIGHT_GRN)
            multiRect  =multiTxt.get_rect(center=(1000,150))
            ekran.blit(multiTxt,multiRect)

            self.resetB  =Button(image=pygame.image.load("datas/redbox.png"),  pos=(1000,300), textInput="Reset", font=pygame.font.Font("datas/font.ttf",43), baseColor=RUSTY_R, hoveringColor=SAFFRON_YLLW)
            self.quitB   =Button(image=pygame.image.load("datas/blackbox.png"),pos=(1000,500), textInput="Quit",  font=pygame.font.Font("datas/font.ttf",40), baseColor=BLACK,   hoveringColor=SAFFRON_YLLW)

            for button in [self.resetB,self.quitB]:
                button.hoverColor(mouse)
                button.update(ekran)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if mouse[0]>800 and self.resetB.checkMouse(mouse):
                        self.resetGame()
                        multiG.resetGame()
                    
                    if mouse[0]>800 and self.quitB.checkMouse(mouse):
                        pygame.quit()
                        sys.exit()

                    if mouse[0]<800 and mouse[1]<800:
                        row   =mouse[1]//SQSIZE
                        col   =mouse[0]//SQSIZE

                        if multiG.emptySquare(row,col) and self.run:
                            self.playerMove(row,col)
                            if self.gameOver():
                                self.run=False
            
            pygame.display.update()


class ComputerMode(Mode):
    def __init__(self,diff:str) -> None:
        super().__init__(mode='AI')
        self.ai_oyuncu  =2
        self.zorluk     =diff
        self.gamePlay(diff)

    def gamePlay(self,zorluk:str):
        ekran     =pygame.display.set_mode((1200,800))
        self.drawGrid()

        while True:
            aiG    =self.gamegrid
            mouse  =pygame.mouse.get_pos()
            aiTxt  =pygame.font.Font("datas/font.ttf",40).render("AI : {}".format(zorluk),True,MIDNIGHT_GRN)
            aiRect =aiTxt.get_rect(center=(1000,150))
            ekran.blit(aiTxt,aiRect)

            self.resetB  =Button(image=pygame.image.load("datas/redbox.png"),  pos=(1000,300), textInput="Reset",  font=pygame.font.Font("datas/font.ttf",43), baseColor=RUSTY_R,   hoveringColor=SAFFRON_YLLW)
            self.changeB =Button(image=pygame.image.load("datas/bluebox.png"), pos=(1000,450), textInput="Change", font=pygame.font.Font("datas/font.ttf",38), baseColor=NAVY_BLUE, hoveringColor=SAFFRON_YLLW)
            self.quitB   =Button(image=pygame.image.load("datas/blackbox.png"),pos=(1000,600), textInput="Quit",   font=pygame.font.Font("datas/font.ttf",41), baseColor=BLACK,     hoveringColor=SAFFRON_YLLW)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for button in [self.resetB,self.changeB,self.quitB]:
                    button.hoverColor(mouse)
                    button.update(ekran)
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if mouse[0]>800 and self.resetB.checkMouse(mouse):
                        self.resetGame(zorluk=zorluk)
                        aiG =self.gamegrid
                    
                    if mouse[0]>800 and self.changeB.checkMouse(mouse):
                        newDiff="Hard" if zorluk=="Easy" else "Easy"
                        self.resetGame(zorluk=newDiff)
                        aiG =self.gamegrid
                    
                    if mouse[0]>800 and self.quitB.checkMouse(mouse):
                        pygame.quit()
                        sys.exit()

                    if mouse[0]<800 and mouse[1]<800:
                        row  =mouse[1]//SQSIZE
                        col  =mouse[0]//SQSIZE

                        if aiG.emptySquare(row,col) and self.run:
                            self.playerMove(row,col)
                            if self.gameOver():
                                self.run=False
            
            if self.mode=="AI" and self.oyuncu==self.ai_oyuncu and self.run:
                pygame.display.update()
                row,col=self.degerlendirme(aiG)
                self.playerMove(row,col)
                if self.gameOver():
                    self.run=False
            
            pygame.display.update()

    def rastgele(self,grids:Grid):
        temp_grids =grids.getEmptySquare()
        num        =random.randrange(0, len(temp_grids))
        return temp_grids[num]

    def minimaxAlgo(self,grids:Grid,max:bool):
        default=grids.winning()

        if default==1:
            return 1,None
        elif default==2:
            return -1,None
        
        elif grids.fullGrid():
            return 0,None
        
        if max:
            max_no  =-100
            bestMax =None
            temp    =grids.getEmptySquare()

            for (row,col) in temp:
                tempGrid  =copy.deepcopy(grids)
                tempGrid.markedGrid(row,col,1)
                num  =self.minimaxAlgo(tempGrid,False)[0]

                if num>max_no:
                    max_no  =num
                    bestMax =(row,col)

            return max_no,bestMax

        elif not max:
            min_no  =100
            bestMin =None
            temp    =grids.getEmptySquare()

            for (row,col) in temp:
                tempGrid  =copy.deepcopy(grids)
                tempGrid.markedGrid(row,col,self.ai_oyuncu)
                num       =self.minimaxAlgo(tempGrid,True)[0]

                if num<min_no:
                    min_no  =num
                    bestMin =(row,col)
            
            return min_no,bestMin

    def degerlendirme(self,gamegrids:Grid):
        if self.zorluk=="Easy":
            val  ="random"
            move =self.rastgele(gamegrids)

        elif self.zorluk=="Hard":
            val,move=self.minimaxAlgo(gamegrids,False)
        
        return move

    def resetGame(self,zorluk:str):
        self.__init__(diff=zorluk)


def AIGame(diff:str):
    compG=ComputerMode(diff=diff)

def MULTIGame():
    multiP=MultiplayerMode()
