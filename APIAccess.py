import requests

BASE_URL = 'https://api.spotify.com/v1/'

class APIAccess:
    def __init__(self, access_token):
        self.headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        self.limit = 50

    def getUserTracks(self):
        cond = True
        informed = False
        offset = 0
        res = []
        
        print("Getting tracks from your library (may take some time)...")
        while (cond):
            r = requests.get(BASE_URL + "me/tracks", headers = self.headers, params = {
                "limit": self.limit, 
                "offset": offset
            })
            r = r.json()

            if ("error" in r):
                print("Not a valid token")
                return None
            elif (r['next'] == None):
                cond = False

            tracks = [{
                "id": t["id"],
                "name": t["name"],
                "artist": {
                    "id": t["artists"][0]["id"],
                    "name": t["artists"][0]["name"]
                }
            } for t in [i["track"] for i in r["items"]]]
            feats = self.getTracksFeatures([t["id"] for t in tracks])

            res += [{**tracks[i], **feats[i]} for i in range(len(tracks))]
            offset = r["offset"] + self.limit
            if (not(informed) and offset > r["total"] / 2):
                print("Almost there, 50% done !")
                informed = True
        print("Done.")
        return res

    def getTracksFeatures(self, ids):
        r = requests.get(BASE_URL + "audio-features", headers=self.headers, params={"ids": ",".join([str(id) for id in ids])})
        r = r.json()
        res = [{"analysis":{ k: f[k] for k in ["danceability", "instrumentalness", "valence"] }} for f in r["audio_features"]]
        return res
