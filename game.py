from os import system, name 

from room import Room
from parser_commands import Parser
from player import Player

class Game():
    PLAYER_NAME = 'Niko'
    PLAYER_WEIGHT = 25
    MOVE_LIMIT = 20
    
    def __init__(self):
        self.player = Player(self.PLAYER_NAME, self.PLAYER_WEIGHT)
        self.createRooms()
        self.parser = Parser()
        self._moves = self.MOVE_LIMIT
        self.stackRooms = []
        self.currentCommand = None
        self.actions = self.createActions()
    
    def createActions(self):
        return {
            "go": self.goRoom,
            "help": self.printHelp,
            "quit": self.quit,
            "look": self.look,
            "back": self.back,
            "eat": self.eat,
            "items": self.items,
            "take": self.take,
            "drop": self.drop
        }
        
    def createRooms(self):
        # ROOMS
        outside = Room("outside the main entrance of the university")
        theater = Room("in a lecture theater")
        pub = Room("in the campus pub")
        lab = Room("in a computing lab")
        office = Room("in the computing admin office")
        laberinth = Room("in the University Labyrinth")
        cellar = Room("in the cellar")
        library = Room("a big, library. Silence are emanating from deep within.")
        kitchen = Room("an small kitchen.")
        kiosk = Room("a small kiosk.")

        #ITEMS
        outside.setItem('apple', 'A red apple', 1, True)
        theater.setItem('mask', 'A horrible mask', 1.5)
        pub.setItem('beer', 'Cold beer', 1)
        pub.setItem('jar', 'But the jar is dirty', 2)
        lab.setItem('microscope', 'A microscope in good condition', 4)
        office.setItem('desk', 'A desk full of papers', 20)
        kitchen.setItem('chicken', "The chicken doesn't look very good", 5, True)
        library.setItem('book','An old, dusty book bound in gray l eather', 2)
        laberinth.setItem('knife', 'The knife looks like it has blood', 3)
        laberinth.setItem('cookie', 'A magic cookie', 4, True)
        
        #EXITS
        outside.setExit('north', laberinth) 
        outside.setExit('east', theater) 
        outside.setExit('west', pub)
        
        theater.setExit('west', outside)
        theater.setExit('up', lab)
        
        pub.setExit('east', outside) 
        pub.setExit('west', laberinth) 
        
        lab.setExit('east', office)
        lab.setExit('down', theater)
        
        office.setExit('east', kiosk)
        office.setExit('west', lab)
        office.setExit('up', laberinth)
        
        laberinth.setExit('east', pub)
        laberinth.setExit('south', outside)
        laberinth.setExit('down', office)
        
        cellar.setExit('south', office)
        cellar.setExit('down', kitchen)
        
        library.setExit('east', kiosk)
        library.setExit('west', kitchen)
        
        kitchen.setExit('east', library)
        kitchen.setExit('south', kiosk)
        kitchen.setExit('up', cellar)
        
        kiosk.setExit('north', kitchen)
        kiosk.setExit('south', office)
        kiosk.setExit('west', library)

        self.player.currentRoom = outside
        
        return
    
    def handleAction(self, command):
        self.clear()
        action = self.actions.get(command)
        #Ejecutamos función del comando
        wantToQuit = action()
        return wantToQuit

    def play(self):
        self.printWelcome()
        finished = False
        while(not (finished) or (finished == None)):
            if(self._moves == 0):
                self.errorMsg("Number of movements exceeded!")
                break
            command = self.parser.getCommand()
            self.currentCommand = command
            finished = self.processCommand(command)
        print("\033[3;35m" + "Thank you for playing, " + self.PLAYER_NAME + ". Good bye." + "\033[0;m")
        print()

    def printWelcome(self):
        self.clear()
        print("\033[1;34m")
        print("Welcome to the World of Zuul, " + self.PLAYER_NAME + "!")
        print("World of Zuul is a new, incredibly boring adventure game." + "\033[0;m")
        print()
        print("\033[1;37m" + "Type 'help' if you need help." + "\033[0;m")
        print('')
    
    def processCommand(self,command):
        #Comando desconocido
        if(command.isUnknown()):
            self.errorMsg("I don't know what you mean...")
            return False
        commandWord = command.getCommandWord()
        return self.handleAction(commandWord)
    
    def hasSecondWord(self):
        if(not self.currentCommand.hasSecondWord()):
            word = self.currentCommand.getCommandWord()
            self.errorMsg("{} what?".format(word.capitalize()))
            return False
        return True
        
    def eat(self):
        if (self.hasSecondWord()):
            item_name = self.currentCommand.getSecondWord()
            item = self.player.getItemByName(item_name)
            if (item == None):
                self.errorMsg("Item does not exist!")
                return
            elif(not item.isEdible()):
                self.errorMsg("I can't eat that...")
                return
            pc = self.player.eat(item)
            self.successMsg("{} eaten!".format(item.name))
            if(pc < 0):
                self.errorMsg("Uups! it has had a negative effect...") 
                
    def take(self):
        if (self.hasSecondWord()):
            item_name = self.currentCommand.getSecondWord()
            currentRoom = self.player.currentRoom
            item = currentRoom.getItemByName(item_name)
            if (item == None):
                self.errorMsg("Item does not exist!")
                return
            #Agregamos al inventario
            result = self.player.takeItem(item) 
            if (result):
                self.successMsg("Item added to inventory!")
            else:
                self.errorMsg("You can't add the object, it exceeds the weight limit")
            
    def drop(self):
        if (self.hasSecondWord()):
            item_name = self.currentCommand.getSecondWord()
            item = self.player.getItemByName(item_name)  
            if (item != None):
                self.player.dropItem(item)
                self.successMsg("Item dropped!")
                return
            self.errorMsg("Item does not exist!")
        
    def back(self):
        try:
            self.player.currentRoom = self.stackRooms.pop()
            self.decrementMove()
            self.look()
        except IndexError as err:
            self.errorMsg("There is no way back!")
               
    def clear(self): 
        # para windows 
        if name == 'nt': 
            _ = system('cls') 
        # para linux/mac
        else: 
            _ = system('clear') 
        
    def printHelp(self):
        print("\033[1;37m" + "You are lost. You are alone. You wander")
        print("around at the university.")
        print()
        print("Your command words are: " + "\033[0;m" + self.parser.show_commands())
        print()

    def goRoom(self):
        if (self.hasSecondWord()):
            direction = self.currentCommand.getSecondWord()
            currentRoom = self.player.currentRoom
            nextRoom = self.player.currentRoom.searchExit(direction) # Buscar la sala
            if(nextRoom != None):
                self.stackRooms.append(currentRoom) # Apilamos al stack
                self.player.currentRoom = nextRoom  # Y asignamos a la sala actual
                self.decrementMove()                # Decrementar numero de movimientos
                self.look()
            else:
                self.errorMsg("There is no door!")
 
    def decrementMove(self):
        self._moves -= 1
        
    def quit(self):
        command = self.currentCommand
        if(command.hasSecondWord()):
            self.errorMsg("Quit what?")
            return False
        else:
            return True
    
    def look(self):
        print(self.player.currentRoom.getDescription())
        print(self.player.currentRoom.showAllItems())
         
    def items(self):
        print(self.player)
        print("\033[1;34m" + "            Available movements: " + str(self._moves) + "\033[0;m")
        print()
    
    def successMsg(self, text):
        print("\033[1;35m" + text + "\033[0;m")
        print()
    
    def errorMsg(self, text):
        print("\033[1;31m" + text + "\033[0;m")
        print()

g = Game()
g.play()