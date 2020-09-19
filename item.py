class Item:
    def __init__(self, name, description, weight, edible=False):
        self._name = name
        self._description = description
        self._weight = weight
        self._edible = edible
    
    @property
    def name(self):
        return self._name
    
    @property
    def weight(self):
        return self._weight
    
    def isEdible(self):
        return self._edible
    
    def __str__(self):
        return '           [' + 'Name: ' + self._name + ', Description: ' + self._description + ', weight: ' + str(self._weight) + ' Kg' + '.]\n'