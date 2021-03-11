from playlist_explanation.src.run.test_3 import run
from playlist_explanation.src.interestingness.interestingness_GB import best_interestingness_weights

if __name__ == "__main__":
    track_name=input("Insert song name: ")
    artist_name=input("Insert artist name: ")
    d = run(best_interestingness_weights(), 'short',
            d={"track_name": track_name, "artist_name": artist_name})
    print(f"{track_name} by {artist_name}")
    print(f"^ {d['segues'][0]['line']}")
    print(f"{d['track_name_2']} by {d['artist_name_2']}")