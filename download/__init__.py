import requests


if __name__ == "__main__":
    r = requests.get('http://www.duckduckgo.com')
    print(r.status_code)
