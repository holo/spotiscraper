import requests, math, os

cyan = '\033[36m'
off = '\033[0m'

class Track:
	def __init__(self, songname, artistname, albumname, cover, url):
		self.songname = songname
		self.artistname = artistname
		self.albumname = albumname
		self.cover = cover
		self.url = url

def ui():
	os.system('cls' if os.name in ('nt', 'dos') else 'clear')
	print(rf""" 
			         _   _                               
		                | | (_)                              
		 ___ _ __   ___ | |_ _ ___  ___ _ __ __ _ _ __   ___ 
		/ __| '_ \ / _ \| __| / __|/ __| '__/ _` | '_ \ / _ \
		\__ \ |_) | (_) | |_| \__ \ (__| | | (_| | |_) |  __/
		|___/ .__/ \___/ \__|_|___/\___|_|  \__,_| .__/ \___|
		    | |                                  | |         
		    |_|              by {cyan}alf{off}              |_|         """)
	print()

def get_token():
	r = requests.get("https://open.spotify.com/get_access_token?reason=transport&productType=web_player")
	return {"Authorization": "Bearer " + r.json()["accessToken"]}

def get_i(playlistid, headers):
	r = requests.get(f"https://api.spotify.com/v1/playlists/{playlistid}", headers=headers)
	return math.ceil(r.json()["tracks"]["total"]/100)

def scrape(playlistid, headers, i):
	scraped = []
	for offset in range(i):
		offset *= 100
		tracks = requests.get(f"https://api.spotify.com/v1/playlists/{playlistid}/tracks/?offset={offset}", headers=headers).json()["items"]

		for track in tracks:
			track = track["track"]
			try:
				cover = track["album"]["images"][0]["url"]
			except:
				cover = ""
			scraped.append(Track(track["name"], track["artists"][0]["name"], track["album"]["name"], cover, f'https://open.spotify.com/track/{track["id"]}'))
	return scraped

def formattrack(format, t):
	formatted = format.replace("$title", t.songname).replace("$artist", t.artistname).replace("$album", t.albumname).replace("$cover", t.cover).replace("$url", t.url)
	return formatted

if __name__ == "__main__":
	ui()
	playlistid = input(f"		    [{cyan}!{off}] Playlist ID{cyan}:{off} ")
	print(f"		    [{cyan}*{off}] Scraping{cyan}...{off}")

	if playlistid.startswith("https://"):
		playlistid = playlistid.split("?")[0].split("/playlist/")[1]

	headers = get_token()
	i = get_i(playlistid, headers)
	tracks = scrape(playlistid, headers, i)

	ui()
	print(f"		    [{cyan}*{off}] Variables")
	print(f"		    [{cyan}*{off}] {cyan}${off}title {cyan}${off}artist {cyan}${off}album {cyan}${off}cover {cyan}${off}url")
	format = input(f"\n		    [{cyan}!{off}] Format{cyan}:{off} ")

	with open("output.txt", "a", encoding="utf-8") as f:
		for t in tracks:
			f.write(formattrack(format, t)+"\n")

	ui()
	print(f"		    [{cyan}*{off}] Successfully wrote to {cyan}output.txt{off}")
	input()