class CommandWords:
    
    def __init__(self):
        pass

    VALID_COMMANDS = ["go", "quit", "help", "look", "back", 'take', 'drop', 'eat', 'items']

    def isCommand(self, aString):
        return aString in self.VALID_COMMANDS
    
    def getCommands(self):
        return self.VALID_COMMANDS
    
    def getCommandList(self):
        return "\033[1;32m" + "[" + ', '.join(self.VALID_COMMANDS) + ']' + '\033[0;m' 