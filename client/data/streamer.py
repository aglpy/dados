
def send(table, player, points, dices, password, show, say):
    table.put_item(Item={'player':player, 'points':points, 'dices':dices, 'password':password, 'show':show, 'say':say})

def send_d(table, d):
    table.put_item(Item=d)

def get_data(table):
    return table.scan().get('Items')