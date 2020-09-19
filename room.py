from item import Item

class Room:
    def __init__(self, description):
        self._description = description
        self._exits = dict()
        self._items = []
    
    def setExit(self, key, value):
        self._exits.setdefault(key, value)
        return
    
    def getExit(self, point):
        return self._exits.get(point) 
    
    def searchExit(self, direction):
        exit = None
        for point in self._exits:
            if (direction == point):
                return self.getExit(point)
        return exit
          
    def getLocation(self):
        cad = 'Exits: \n'
        return "\033[1;33m" + cad + '      [' + ', '.join(self._exits) + ']' + '\033[0;m' 
            
    def getDescription(self):
        return  "\033[1;35m" + "YOU ARE " + self._description.upper() + '.\n' + "\033[0;m" + self.getLocation()
        
    def setItem(self, name, description, weight, edible=False):
        item = Item(name, description, weight, edible)
        items = self._items
        items.append(item)
        
    def addItem(self, item):
        #Para agregar objeto item ya existente
        items = self._items
        items.append(item)
        
    def removeItem(self, item):
        items = self._items
        items.remove(item)
    
    def getItemByName(self, name):
        for item in self._items:
            if ( item.name == name):
                return item
        return None
        
    def showAllItems(self):
        print()
        cad = "\033[1;36m" + 'Room Items: \n'
        items = self._items
        lenItems = len(items)
        if (lenItems == 0):
            return cad + '           [Empty]' + "\033[0;m"
        else:
            for item in items:
                cad = cad + str(item)
            return cad + "\033[0;m"
        