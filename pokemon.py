import requests, pprint, json
from IPython.display import clear_output
# data = requests.get('https://pokeapi.co/api/v2/')




# pokemons = data.json()
pp = pprint.PrettyPrinter(indent=4)
class Pokemon:
    def __init__(self, name=None, abilities=None, types=None, height=None, weight=None):
        self.name = name
        if abilities is None:
            self.abilities = []
        if types is None:
            self.types = []
        self.height = height
        self.weight = weight

    def from_dict(self, data):
        for field in ['name', 'abilities', 'types', 'height', 'weight']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return f'<Pokemon>: {self.name}'

    def __str__(self):
        return f'{self.name}'

class Pokedex:
    _list = []

    @classmethod
    def show(cls):
        print('=~'* 50)
        for idx, p in enumerate(cls._list):
            print(f'{idx+1}: {p}')
        print('=~'* 50)
 
    @classmethod
    def instructions(cls):
        print("""Type 'show' to view Pokedex
Type 'quit' to exit the Pokedex
Type 'sort' to view a category 
        """)
 
    @classmethod
    def add(cls, pokemon_name):
        if cls._list:
            for p in cls._list:
                if pokemon_name.title() == p.name:
                    input ("That pokemon already exists. Please try adding another: ")
                    return
    
        try:
            print('Please wait while we populate the Pokedex...')
            r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}').json()
            
            p = Pokemon()
            data_dict = {
                'name': r['name'].title(),
                'abilities': [a['ability']['name'].title() for a in r['abilities']],
                'types': [t['type']['name'].title() for t in r['types']],
                'height': r['height'],
                'weight': r['weight']
            }
            p.from_dict(data_dict)
            cls._list.append(p)

        except:
            input("There was an error populating your Pokedex. Please try again: ")

    @classmethod
    def sort(cls):
        sorted_dict = {}

        for p in cls._list:
            for t in p.types:
                if t not in sorted_dict:
                    sorted_dict[t] = {}

        for p in cls._list:
            for t in p.types:
                if p.name not in sorted_dict[t]:
                    poke_data = {
                        p.name: {
                            'abilities' : p.abilities,
                            'height' : p.height,
                            'weight' : p.weight,                       
                        }
                    }
                    sorted_dict[t].update(poke_data)
                else:
                    print("That Pokemon already exists")
        pp.pprint(sorted_dict)

    @classmethod
    def run(cls):
        done = False

        while not done:
            clear_output()

            print(cls._list)

            cls.instructions()

            pokemon_choice = input("Type in the name of the Pokemon you wish to add. Type 'quit' to exit the program: ").lower()
            if pokemon_choice == 'quit':
                done = True
            elif pokemon_choice == 'show':
                cls.show()
                input('Press "ENTER" to continue')
            elif pokemon_choice == "sort":
                cls.sort()
                input('Press "Enter" to continue: ')
            else:
                cls.add(pokemon_choice)
Pokedex.run()

