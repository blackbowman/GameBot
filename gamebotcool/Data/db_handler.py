import os
import pickle as pk


def add_inscriptions(user : str):
    liste = []
    liste.append(user)
    try:
        with open(os.chdir("/home/blackbowman/Blackbowman/pyprograms/gamebotcool/Data/database.txt"), 'ab') as datafile:
            data = pk.Pickler(datafile)
            data.dump(liste)
            data.close()
    except Exception as e:
        print(e)

def clear_db(channel_id):
    try:
        if channel_id == channel_id:
            pass
        else:
            print("Le salon n'est pas le bon")
        with open(os.chdir("/home/blackbowman/Blackbowman/pyprograms/gamebotcool/Data/database.txt"), 'rb') as datafile:
            data = pk.Unpickler(datafile)
            cdata = data.load()
            cdata.clear()
            pass
    except Exception as e:
        print(e)