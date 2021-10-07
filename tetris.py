# Name: Soon Sam R Santos
# Date: February 08, 2017 - Feb. 09,
# Session: Final Project
# tetris.py

from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)    # self is my block. self = Rectangle...
        self.setWidth(Block.OUTLINE_WIDTH)  # The outline width will appear in the lower right corner.
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''
        #YOUR CODE HERE
        sup_x = self.x + dx 
        sup_y = self.y + dy   
        # Calls Board to check if I can move the block to the sup_x, sup_y position on the board (self.board).
        if Board.can_move(board, sup_x, sup_y):
            return True
        else:
            return False
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        #This is to change the position of the block, otherwise the second time to move would not properly work.
        self.x += dx
        self.y += dy
        # This is to move the Rectangle dx and dy units. *Block.BLOCK_SIZE is to pass to pixels.
        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        
        for pos in coords:
            # Coords contain the Points to make the shapes.
            # self.block contain the true Blocks.
            self.blocks.append(Block(pos, color))



    def get_blocks(self):
        '''returns the list of blocks
        '''
        #YOUR CODE HERE
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

    def undraw(self):
        for block in self.blocks:
            block.undraw()
            
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            # Using the Block (move method) to move each block of the shape.
            # As the result, the shape as a whole will move.
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise
           
        '''
        
        #YOUR CODE HERE
        count = 0
        for block in self.blocks:
            # This can_move is from Block and it needs a board as a parameter.
            if Block.can_move(block, board, dx, dy):
                count = count + 1
        if count == len(self.blocks):
            return True
        else:
            return False
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return -self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        #YOUR CODE HERE
        d = self.get_rotation_dir()
        count = 0
        for block in self.get_blocks():
            # The center block will just move to the same square.
            x = self.center_block.x -(d*self.center_block.y) + (d*block.y)
            y = self.center_block.y + (d*self.center_block.x) - (d*block.x)
            if Board.can_move(board, x, y):
                count = count + 1
        if count == len(self.get_blocks()):
            return True
        return False
            
    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
            
        '''    

        ####  YOUR CODE HERE #####
        d = self.get_rotation_dir()
            
        for block in self.get_blocks():
            x = self.center_block.x -(d*self.center_block.y) + (d*block.y)
            y = self.center_block.y + (d*self.center_block.x) - (d*block.x)
            # The new position minus the old position is the quantity of units the block needs to move.
            Block.move(block, (x - block.x), (y - block.y))

        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

        

############################################################
# ALL SHAPE CLASSES
############################################################

# Counterclockwise then clockwise.
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        # I is lying down. It is not standing.
        # self.blocks is the list with the blocks that form the shape.
        # self.center_block is receiving the block in the middle.
        self.center_block = self.blocks[2]

# Always rotate clockwise.
class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        
        self.center_block = self.blocks[1]

# Always rotate clockwise.
class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')        
        self.center_block = self.blocks[1]

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        # I need to set the center_block because it is it that is going to move
        self.center_block = self.blocks[0]
    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return
# Clockwise then Counterclockwise.
class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

# Always rotate clockwise.
class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]

# Clockwise then Counterclockwise.
class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1      



############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    SCORE_WIDTH = 6
    SCORE_HEIGHT = 3
    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        # It draws a CanvaFrame in the window and the CanvaFrame object shapes will be draw on the CanvasFrame.
        # Preview board is the top (fisrt).
        self.preview_board = PiecePreview(win, Tetris.BOARD_WIDTH, self.SCORE_HEIGHT)
        # The big board is in the middle (second).
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')
        self.points = 0
        # The scores are called last so they are at the bottom (third).
        self.score_board = ScoreBoard(win, self.SCORE_WIDTH, self.SCORE_HEIGHT)
        # create an empty dictionary
        # currently we have no shapes on the board
        # key: tuple --> string(x,y) Value : Block object 
        self.grid = {}

    def draw_shape(self, shape):   # self here is the board.
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        self.game_over()
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
            
        '''
            
        #YOUR CODE HERE
        # If the position is outside of the board boundaries
        if x<0 and y in range(-1,21):
            return False
        if x>9  and y in range(-1,21):
            return False
        if x in range(-1,21) and y>19:
            return False

        # If there is already a block at that position.
        
        # Creating a sup object which receive the string where the block is trying to go.
        sup_string = '('+str(x)+','+str(y)+')'
        # If this string is already in the values it means there is some block there, therefore it can not move.
        if sup_string in self.grid.keys():
            return False
        return True
    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        
        #YOUR CODE HERE       
        for block in Shape.get_blocks(shape):
            x = block.x
            y = block.y
            self.grid['('+str(x)+','+str(y)+')'] = block
     

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout
            
        '''
        
        #YOUR CODE HERE
        if self.is_row_complete(y):
            for x in range(10):
                block = self.grid['('+str(x)+','+str(y)+')']
                del self.grid['('+str(x)+','+str(y)+')']
                block.undraw()
            
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        
        #YOUR CODE HERE
        count = 0
        for x in range(10):  # x goes from 0 to 9.
            if '('+str(x)+','+str(y)+')' in self.grid.keys():
                count += 1
        if count==10:
            return True
        return False
    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        
        #YOUR CODE HERE
        # Assuming y_start = 6
        sup_list = []
        # num from 0 to 6.
        for num in range(y_start + 1):
            # list with 7 positions, begin = 7 finish = 0
            sup_list.append(y_start - num)  
        y = 0
        # Run 7 times. y = 0 until y = 6
        while y<=y_start:
            for x in range(10):
                # sup_list[0] is 6. until sup_list[6] = 0
                if '('+str(x)+','+str(sup_list[y])+')' in self.grid.keys():
                    block = self.grid['('+str(x)+','+str(sup_list[y])+')']
                    del self.grid['('+str(x)+','+str(sup_list[y])+')']
                    Block.move(block, 0, 1)
                    self.grid['('+str(x)+','+str(sup_list[y] + 1)+')'] = block
            y = y + 1
    
    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''
        
        #YOUR CODE HERE
        count = 0
        for y in range(20):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.move_down_rows(y - 1)
                count += 1
        # Counting the points accordingly with the quantity of rows complet at once.
        if count==1:
            ScoreBoard.undraw_score(self.score_board)
            self.points += 10
            ScoreBoard.draw_points(self.score_board, self.points)
        if count==2:
            ScoreBoard.undraw_score(self.score_board)
            self.points += 20
            ScoreBoard.draw_points(self.score_board, self.points)
        if count==3:
            ScoreBoard.undraw_score(self.score_board)
            self.points += 30
            ScoreBoard.draw_points(self.score_board, self.points)
        if count>=4:
            ScoreBoard.undraw_score(self.score_board)
            self.points += 40
            ScoreBoard.draw_points(self.score_board, self.points)

    def pause_game(self):
        
        self.pause = Text(Point(self.canvas.width*0.5,self.canvas.height*0.5), "PAUSE")
        self.pause.setSize(30)
        self.pause.draw(self.canvas)

    def start_game(self):
        self.pause.undraw()
        # Now I need to stop everything working.
               
    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        
        #YOUR CODE HERE
        game_over = Text(Point(self.canvas.width*0.5,self.canvas.height*0.5), "GAME OVER")
        game_over.setSize(30)
        game_over.draw(self.canvas)

class ScoreBoard():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                  self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')
        # I must draw the text above the canvas frame and not above the window.
        self.draw_score()
        self.draw_points(0)

    def draw_score(self):
        # I was taking the win as a parameter, but I don't need, as the win is already self.canvas
        self.text = Text(Point(self.canvas.width*0.2, self.canvas.height*0.5), "SCORE:")
        self.box = Rectangle(Point(self.canvas.width*0.4, self.canvas.height*0.2), Point(self.canvas.width*0.85, self.canvas.height*0.75))
        self.box.setFill('black')
        self.text.draw(self.canvas)
        self.box.draw(self.canvas)
    def draw_points(self, x):
        self.points = Text(Point(self.canvas.width*0.7, self.canvas.height*0.5),str(x))
        self.points.setFill('yellow')
        self.points.draw(self.canvas)
    def undraw_score(self):
        self.points.undraw()

class PiecePreview():
    # Initializating a canvas to draw the preview shape.
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.canvas = CanvasFrame(win, self.width*Block.BLOCK_SIZE,
                                  self.height*Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')
        
    def draw_P_shape(self, shape):   # self here is the preview_board.
        
        shape.draw(self.canvas)

                
###########################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000 #ms
        self.game = 'playing'

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        
        self.current_shape = self.create_new_shape()
        
        # set the preview shape to a random new shape
        self.preview_shape = self.create_new_shape()

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        ####  YOUR CODE HERE ####
        Board.draw_shape(self.board, self.current_shape)
        #Drawing the preview shape on the preview board.
        PiecePreview.draw_P_shape(self.board.preview_board, self.preview_shape)
        
        # For Step 9:  animate the shape!
        ####  YOUR CODE HERE ####
        # The code was ready, it was just necessary to call it.
        self.animate_shape()


    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        # random.randint(from, to) Both inclusive
        # Tetris.SHAPE
        # SHAPES contain 7 blocks. 0 to 6 position
        #YOUR CODE HERE
        num = random.randint(0,6)
        # self here is the board. x is going to be the 5, this is in the middle of the board
        new_shape = Tetris.SHAPES[num](Point(int(self.BOARD_WIDTH/2),0))
        return new_shape

        
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        if self.game == 'playing':
            self.do_move('Down')
            # The up levels here is working
            # but these values is just for test.
            # You just need a text now to display in what nivel you are!
            if self.board.points == 10:
                self.delay = 500
            if self.board.points == 20:
                self.delay = 200
            self.win.after(self.delay, self.animate_shape)
        
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        '''
        
        #YOUR CODE HERE
        # 1 - Condition to the directions.
        # 2 - Condition if the shape can move or not.
        # 3 - Moving and returning True.
        if self.game == 'playing':
            if direction == 'Right':
                if Shape.can_move(self.current_shape, self.board, Tetris.DIRECTION['Right'][0], Tetris.DIRECTION['Right'][1]):
                    Shape.move(self.current_shape, (Tetris.DIRECTION['Right'][0] ), (Tetris.DIRECTION['Right'][1] ))
                    return True
                
            if direction == 'Left':
                if Shape.can_move(self.current_shape, self.board, Tetris.DIRECTION['Left'][0], Tetris.DIRECTION['Left'][1]):
                    Shape.move(self.current_shape, Tetris.DIRECTION['Left'][0], Tetris.DIRECTION['Left'][1])
                    return True

            if direction == 'Down':
                if Shape.can_move(self.current_shape, self.board, Tetris.DIRECTION['Down'][0], Tetris.DIRECTION['Down'][1]):
                    # if the shape is in the last place a the the direction to move was down, I'll add this to the grid (add_shape)
                    Shape.move(self.current_shape, (Tetris.DIRECTION['Down'][0] ), Tetris.DIRECTION['Down'][1])
                    return True
                else:
                    # The shape can't move when I press down and it is in the bottom or when some piece is overboard.
                    # 1 - Add the last shape to board.grid. 
                    Board.add_shape(self.board, self.current_shape)
                    # 2 - Remove the complete rows, if any.
                    Board.remove_complete_rows(self.board)
                    # 3 - The current shape receive the preview shape.
                    self.current_shape = self.preview_shape
                    # 4 - Undraw the preview shape from the preview board.
                    Shape.undraw(self.preview_shape)
                    # 5 - Draw the current shape on the board.
                    Board.draw_shape(self.board, self.current_shape)
                    # 6 - Receive a new preview shape.
                    self.preview_shape = self.create_new_shape()
                    # 7 - Draw the new preview shape on the preview board, only if the game is not over.
                    if Shape.can_move(self.current_shape, self.board, 0, 0):
                        PiecePreview.draw_P_shape(self.board.preview_board, self.preview_shape)
                    # 8 - Return false.
                    return False
                    
        return False
    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        
        #YOUR CODE HERE
        # Why can I can can_rotate and rotate righ here in Tetris without Shape.method...
        if self.current_shape.can_rotate(self.board) and self.game == 'playing':
            self.current_shape.rotate(self.board)
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
            
        #YOUR CODE HERE
        # key is receiving the string value of the key pressed.
        # 'Up', 'Down', 'Left', 'Right' are the special values for the arrow keys and space bar.
        key = event.keysym
        # key is the direction to move
        if key == 'space' and self.game == 'playing':
            # sup_y is the quantity of times the piece needs to move until the bottom.
            sup_y = 19 - self.current_shape.center_block.y
            for i in range(1,sup_y + 1):
                # The shape will move one by one until the bottom sup_y th times.
                # When some piece be in the middle of the path, it will not move until the bottom. It'll stop in the piece.
                if Shape.can_move(self.current_shape, self.board, 0, 1):
                    Shape.move(self.current_shape, 0, 1)
        if key == 'Up':
            self.do_rotate()
        if key == 'p' or key == 'P':
            if self.game == 'playing':
                # pause the game and set the pause message.
                Board.pause_game(self.board)
                self.game = 'pause'
            else:
                # Come back the game and undraw the message.
                Board.start_game(self.board)
                self.game = 'playing'
                self.animate_shape()
        self.do_move(key)
    
       
################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()
