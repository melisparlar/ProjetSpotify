import os
import sys
from APIAccess import APIAccess
from Playlist import Playlist

# création du dossier pour sauvegarder les playlists
os.makedirs("./playlists/", exist_ok=True)

# si le token a été fourni dans les arguments, on l'utilise
api_data = None
if (len(sys.argv) > 1):
    access_token = sys.argv[1]
    api = APIAccess(access_token)
    api_data = api.getUserTracks()

# si le token n'a pas été donné ou s'il est invalide, on le redemande
while (api_data == None):
    access_token = input("Enter a valid token: ")
    api = APIAccess(access_token)
    api_data = api.getUserTracks()
    pass

pl = Playlist(api_data, "all")

print(pl.nb_tracks, "tracks retrieved.")

# boucle principale faisant l'affichage
while (True):
    cmd = input("""\n----- Spotify playlist generator -----
    1 - View stats
    2 - Generate playlist
    3 - Exit
# """)
    if (cmd == "1"):
        print("\n" + pl.getStats())
        input("\nPress a key to continue...")
    elif (cmd == "2"):
        while (True):
            type = input("""
1 - Happy mix
2 - Sad mix
3 - Dance mix
4 - Instrumental mix
5 - Leave
""")
            if (type in ["1", "2", "3", "4"]):
                npl = pl.generatePlaylist(type)
                answer = input(f"Save playlist ({npl.nb_tracks} tracks) ?[Y/n] ")
                if (answer != "n"):
                    npl.save()
            else:
                break
    else:
        break