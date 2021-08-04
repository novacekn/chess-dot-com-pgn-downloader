import argparse
import requests
import os
import sys


def main():
    archives_url = "https://api.chess.com/pub/player/{}/games/archives/"
    parser = argparse.ArgumentParser(description="Download a chess.com user's game PGNs")
    parser.add_argument("Username", metavar="username", type=str, help="chess.com username")
    parser.add_argument("Path", metavar="download_path", type=str, help="path to download PGNs to")

    args = parser.parse_args()

    username = args.Username
    download_path = args.Path

    archives = get_archives(archives_url.format(username))
    get_games(archives, download_path)

    if not os.path.isdir(download_path):
        print("The given path does not exist.")
        sys.exit()


def get_archives(url):
    res = requests.get(url=url).json()["archives"]
    return res


def get_games(archives, download_path):
    games = []
    for archive in archives:
        games.append(requests.get(url=archive).json()["games"])

    for game in games:
        for item in game:
            filename = download_path + "/" + item["white"]["username"] + "_" + item["black"]["username"] + ".pgn"
            f = open(filename, "w+")
            f.write(item["pgn"])
            f.close()


if __name__ == "__main__":
    main()

