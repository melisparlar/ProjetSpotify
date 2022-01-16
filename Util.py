# classe parent pour les éléments de spotify (artistes, musiques, épisodes de podcats, albums...)
class SpotifyObject:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
    
    def __str__(self):
        return self.name

# classe pour les artistes
# elle possède les mêmes attributs que la classe parent
# ici l'héritage aurait été plus util si les genres musicaux des artistes étaient pris en compte (manque de temps)  
class Artist(SpotifyObject):
    def __init__(self, data):
        super().__init__(data)
    
    def __str__(self):
        return super().__str__()
    
    def __eq__(self, obj):
        return isinstance(obj, Artist) and self.id == obj.id

    # surcharge de la fonction de hashage pour pouvoir les compters dans une liste
    def __hash__(self):
        return hash(self.id)

# classe pour les morceaux de musique
# explication de certains attributs :
## danceability -> indice de 0 à 1, quand l'indice s'approche de 1 le morceau est considéré comme dansant 
## instrumentalness -> indice de 0 à 1, si l'indice est proche de 1 le morceau est considéré comme un morceau instrumental
## valence -> indice de 0 à 1, si l'indice est proche de 1, le morceau est considéré comme positif
class Track(SpotifyObject):
    def __init__(self, data):
        super().__init__(data)
        self.artist = Artist(data["artist"])
        self.danceability = data["analysis"]["danceability"]
        self.instrumentalness = data["analysis"]["instrumentalness"]
        self.valence = data["analysis"]["valence"]

    def __str__(self):
        return f"{self.name} - {self.artist}"

    def __eq__(self, obj):
        return isinstance(obj, Track) and self.name == obj.name and self.artist == obj.artist