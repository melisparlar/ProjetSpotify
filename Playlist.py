import json
from Util import Track
import random
from datetime import datetime

class Playlist:
    def __init__(self, data, type):
        self.raw_data = data
        self.tracks = [Track(t) for t in self.raw_data]
        self.artists = [t.artist for t in self.tracks]
        self.nb_tracks = len(self.tracks)
        self.type = type

    def __str__(self):
        return "\n".join(str(t) for t in self.tracks)

    # obtention des stats de la playlist :
    # - Nombre d'artistes différents dans la playlist
    # - Top 10 des artistes par nombre d'apparition dans la playlist  
    def getStats(self):
        # liste des artistes, sans doublon 
        artists_no_dup = list(set(self.artists))

        # dictionnaire avec { artiste: nombre d'apparition }
        artists_count = sorted({str(a):self.artists.count(a) for a in artists_no_dup}.items(), key = lambda x: x[1], reverse = True)

        # mise en forme de la chaine de caractères
        res = "Number of tracks: " + str(self.nb_tracks)
        res += "\nNumber of artists: " + str(len(artists_no_dup))
        res += "\n\nTop 10 artists:\n"
        res += '\n'.join(k + ': ' + str(v) for (k, v) in artists_count[0:10])
        return res

    # génération d'une playlist
    # les 4 types possibles sont :
    # - Mix joyeux
    # - Mix triste
    # - Dansant
    # - Instrumental
    def generatePlaylist(self, type):
        type = int(type)
        criterion = ""
        high_values = True
        threshold = 0.8
        name = ""

        if (type < 3):
            name = "happy_mix"
            criterion = "valence"
            if (type == 2):
                name = "sad_mix"
                threshold = 1 - threshold
                high_values = False
        else:
            if (type == 3):
                name = "dance_mix"
                criterion = "danceability"
            else:
                name = "instrumental_mix"
                criterion = "instrumentalness"

        # tri du dictionnaire des morceaux en fonction de <criterion>, croissant ou non en fonction de <high_values>
        sortd = sorted(self.raw_data, key = lambda t: t["analysis"][criterion], reverse = high_values)
        
        # on ne garde que 20% de la taille de la playlist mère  
        # + si la valeur du est pertinent critère
        ##  ex : si playlist joyeuse, on teste si <valence> > 0.8
        if (type == 2):
            sortd = [t for t in sortd[0:int(self.nb_tracks/5)] if t["analysis"][criterion] < threshold]
        else:
            sortd = [t for t in sortd[0:int(self.nb_tracks/5)] if t["analysis"][criterion] > threshold]

        # on en garde 100 aléatoire (ou moins si pas assez de morceaux) parmis ceux qui correspondent au critère
        play_len = len(sortd) if 100 > len(sortd) else 100
        random.shuffle(sortd)
        return Playlist(sortd[0:play_len], name) 

    # sauvegarde de la playlist au format json et txt
    def save(self):
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = self.type + "_" + date_str

        with open('playlists/' + filename + '.json', 'w+', encoding='utf-8') as f:
            json.dump(self.raw_data, f, ensure_ascii=False, indent=4)
        with open('playlists/' + filename + '.txt', 'w+', encoding='utf-8') as text_file:
            text_file.write(str(self))