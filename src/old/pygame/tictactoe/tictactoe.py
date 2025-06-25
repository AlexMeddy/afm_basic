import pygame 
pygame.init()

XO = 'X' 

winner = None

draw = None

board = [[None]*3, [None]*3, [None]*3] 

clock = pygame.time.Clock()

screen = pygame.display.set_mode((400,400))

pygame.display.set_caption("Tic Tac Toe")

ximg = pygame.image.load("C:\\Users\\alexf\\OneDrive\\Desktop\\src\\pygame\\tictactoe\\X.png")
oimg = pygame.image.load("C:\\Users\\alexf\\OneDrive\\Desktop\\src\\pygame\\tictactoe\\O.png")

ximg = pygame.transform.scale(ximg, (80, 80))
oimg = pygame.transform.scale(oimg, (80, 80))

def drawgrid(): 
	screen.fill((241, 192, 185))
	pygame.draw.line(screen, (236, 248, 127), (400 / 3, 0), (400 / 3, 400), 6)
	pygame.draw.line(screen, (236, 248, 127), ((400 / 3) * 2, 0), ((400 / 3) * 2, 400), 6)

	pygame.draw.line(screen, (236, 248, 127), (0, 400 / 3), (400, 400 / 3), 6)
	pygame.draw.line(screen,(236, 248, 127), (0, (400 / 3) * 2), (400,(400 / 3) * 2), 6)
	

def result():
	global draw,winner
	if winner:
		message = winner + " won!"
	if draw:
		message = "Game Draw!"

	font = pygame.font.SysFont('Georgia', 70)
	text = font.render(message, 1, (24, 154, 180))	
	screen.fill ((0, 0, 0), (0, 400, 500, 100))
	text_rect = text.get_rect(center =(400 // 2, 400//2))
	screen.blit(text, text_rect)
	pygame.display.update()


def wincases(): 
	global board, winner, draw
	for row in range(0, 3):
		if((board[row][0] == board[row][1] == board[row][2]) and (board [row][0] != None)):
			winner = board[row][0]
			pygame.draw.line(screen, (250, 0, 0),(0, (row + 1)*400 / 3 -400 / 6),(400, (row + 1)*400 / 3 - 400 / 6 ),4)
			result()
			break

	for col in range(0, 3):
		if((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] != None)):
			winner = board[0][col]
			pygame.draw.line (screen, (250, 0, 0), ((col + 1)* 400 / 3 - 400 / 6, 0),((col + 1)* 400 / 3 - 400 / 6, 400), 4)
			result()
			break

	if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] != None):

		winner = board[0][0]
		pygame.draw.line (screen, (250, 70, 70), (50, 50), (350, 350), 4)
		result()

	if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] != None):

		winner = board[0][2]
		pygame.draw.line (screen, (250, 70, 70), (350, 50), (50, 350), 4)
		result()
	if(all([all(row) for row in board]) and winner == None ):
		draw = True
		result()
	

def getimg(row, col):
	global board, XO

	if row == 1:
		posy = 30

	if row == 2:
		posy = 400 / 3 + 30

	if row == 3:
		posy = 400 / 3 * 2 + 30

	if col == 1:
		posx = 30

	if col == 2:
		posx = 400 / 3 + 30

	if col == 3:
		posx = 400 / 3 * 2 + 30

	board[row-1][col-1] = XO

	if(XO == 'X'):

		screen.blit(ximg, (posx, posy))
		XO = 'O'

	else:
		screen.blit(oimg, (posx, posy))
		XO = 'X'
	pygame.display.update()

def input_to_block(): 
	x, y = pygame.mouse.get_pos()

	if(x<400 / 3):
		col = 1

	elif (x<400 / 3 * 2):
		col = 2

	elif(x<400):
		col = 3

	else:
		col = None

	if(y<400 / 3):
		row = 1

	elif (y<400 / 3 * 2):
		row = 2

	elif(y<400):
		row = 3

	else:
		row = None

	if(row and col and board[row-1][col-1] is None):
		global XO
		getimg(row, col)
		wincases()

drawgrid() 

while True: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			input_to_block()
			
	pygame.display.update()
	clock.tick(30)