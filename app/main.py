import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

class game_status:
    def __init__(self, data, next_move):
        self.height = data['board']['height']
        self.width = data['board']['width']
        #num_food = len(data['board']['food'])
        self.food = data['board']['food']
        self.me = data['you']
        #num_snakes = len(data['board']['snakes'])
        self.rival = []
        for i in data['board']['snakes']:
            if i['id'] != self.me['id']:
                self.rival.append(i)
                
        self.result = next_move    
        
        self.rank = 0        
        
        self.new_x = 0    
        self.new_y = 0 
        
        if next_move == 'u':
            new_x = data['you']['body'][0]['x']
            new_y = data['you']['body'][0]['y'] - 1
        elif next_move == 'd':
            new_x = data['you']['body'][0]['x']
            new_y = data['you']['body'][0]['y'] + 1
        elif next_move == 'l':
            new_x = data['you']['body'][0]['x'] - 1
            new_y = data['you']['body'][0]['y']
        elif next_move == 'r':
            new_x = data['you']['body'][0]['x'] + 1
            new_y = data['you']['body'][0]['y']
            
        if new_x == self.width - 1 or new_x == 0 or new_y == self.height - 1 or new_y == 0:
            self.rank = 0
        else:
            self.rank = 1
            
        '''if new_y == self.height - 1 or new_y == 0:
            self.rank = 0
        else:
            self.rank = 1'''
                
        self.t = {'x': new_x, 'y': new_y}
        if self.t in data['you']['body']:
            self.rank = -1
            
        if new_x >= self.width or new_x < 0:
            self.rank = -1
            
        if new_y >= self.height or new_y < 0:
            self.rank = -1
            
        for i in range(len(self.rival)):
            if self.t in self.rival[i]['body']:
                self.rank = -1
                
        
        
        
        
@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))
    
    #initialize_global(data)

    color = {"color": "#FFCC00", "headType": "pixel", "tailType": "pixel"}

    return color #start_response(json.dumps(color))


@bottle.post('/move')
def move():
    data = bottle.request.json
    
    me = data['you']
    #num_snakes = len(data['board']['snakes'])
    rival = []
    for i in data['board']['snakes']:
        if i['id'] != me['id']:
            rival.append(i)
    
    
    n = len(rival)
    a = ['u', 'd', 'l', 'r']
    b = ['u', 'd', 'l', 'r']
    if n == 0:
        move_comb = ['u', 'd', 'l', 'r']
    else:
        for k in range(n):
            move_comb = []
            for i in range(len(a)):
                for j in range(len(b)):
                    move_comb.append(a[i] + b[j])
            b = move_comb[:]
        
        
    all_moves = []
    for i in ['u', 'd', 'l', 'r']:
        all_moves.append(game_status(data, i))
        
    nm = 'u'
    final0 = []
    final1 = []
    
    for i in all_moves:
        if i.rank == 0:
            final0.append(i.result)
        if i.rank == 1:
            final1.append(i.result)
    
    if len(final1) != 0:
        nm = random.choice(final1)
    elif len(final0) != 0:
        nm = random.choice(final0)
    else:
        nm = random.choice(['u', 'd', 'l', 'r'])
    
   
    if nm == 'u':
        direction = 'up'
    elif nm == 'd':
        direction = 'down'
    elif nm == 'l':
        direction = 'left'
    else:
        direction = 'right'


    #print(json.dumps(data))

    #directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)
    
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))
    

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
