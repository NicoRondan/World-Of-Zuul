import random

class Player:
    def __init__(self, name, height):
        self._inventory = []
        self._name = name
        self._maxWeight = height
        self._currentRoom = None
    
    @property
    def currentRoom(self):
        return self._currentRoom

    @currentRoom.setter
    def currentRoom(self, room):
        self._currentRoom = room
    
    def eat(self, item):
        maxWeight = self._maxWeight
        value = random.randint(-10, 15)                   # Valor random a sumar o restar del peso límite
        total = maxWeight + ((value * maxWeight) / 100)   # Calculamos el porcentaje y lo sumamos al peso límite
        self._inventory.remove(item)
        self._maxWeight = total
        return value
    
    def takeItem(self, item):
        isFull = self.isFull(item)               #Verificar que el player no supere el peso máximo
        if (isFull):
            return False
        else:
            self._inventory.append(item)         #Agregarlo al inventorio
            self._currentRoom.removeItem(item)   #Y eliminarlo del room actual
            return True
    
    def dropItem(self, item):
            self._inventory.remove(item)         # Eliminamos del inventario
            self._currentRoom.addItem(item)      # Y lo agregamos a la sala actual
                
    def isFull(self, element):
        total = self.totalWeight() + element.weight        # Sumar pesos 
        return total > self._maxWeight                     # Verificar que no sobrepase el peso permitido
    
    def getItemByName(self, name):
        for item in self._inventory:
            if ( item.name == name):
                return item
        return None
    
    def totalWeight(self):
        inventoryWeight = 0
        for item in self._inventory:
            inventoryWeight += item.weight
        return inventoryWeight
    
    def __str__(self):
        cad = "Player's Info: \n"
        aux = [item.name for item in self._inventory]
        cadInventory = 'Empty' if len(aux) == 0 else ', '.join(aux)
        return "\033[1;32m" + cad + '            Inventory: [' + cadInventory + '] \n' + '            Total Weight: ' + str(self.totalWeight()) + 'Kg - Max Weight: ' + str(self._maxWeight) + 'Kg.' + '\033[0;m' 
    
    
   