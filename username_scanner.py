import os
import requests

def banner():
    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Welcome to the username scanner\033[0m")

def partial(username):
    if os.path.exists(f"{username}.txt"):
        print(f"\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Saved:\033[0m\033[1;77m {username}.txt\033[0m")

def check_website(url, username):
    try:
        response = requests.get(url.format(username), headers={'Accept-Language': 'en'}, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        print(f"\033[1;91mError: \033[0m{e}")
        return None

def scanner():
    username = input("\033[1;92m[\033[0m\033[1;77m?\033[0m\033[1;92m] Input Username:\033[0m ")

    if os.path.exists(f"{username}.txt"):
        print(f"\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Removing previous file:\033[0m\033[1;77m {username}.txt")
        os.remove(f"{username}.txt")

    print(f"\n\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Checking username\033[0m\033[1;77m {username}\033[0m\033[1;92m on: \033[0m")

    # List of websites to check
    websites = {
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "Twitter": "https://www.twitter.com/{}",
        "YouTube": "https://www.youtube.com/{}",
        "Blogger": "https://{}.blogspot.com",
        "GooglePlus": "https://plus.google.com/+/{}",
        "Reddit": "https://www.reddit.com/user/{}",
        "Wordpress": "https://{}.wordpress.com",
        "Pinterest": "https://www.pinterest.com/{}",
        "GitHub": "https://www.github.com/{}",
        "Tumblr": "https://{}.tumblr.com",
        "Flickr": "https://www.flickr.com/people/{}",
        "Steam": "https://steamcommunity.com/id/{}",
        "Vimeo": "https://vimeo.com/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Disqus": "https://disqus.com/{}",
        "Medium": "https://medium.com/@{}",
        "DeviantArt": "https://{}.deviantart.com",
        "VK": "https://vk.com/{}",
        "About.me": "https://about.me/{}"
    }

    for site, url in websites.items():
        print(f"\033[1;77m[\033[0m\033[1;92m+\033[0m\033[1;77m] {site}: \033[0m", end="")

        status_code = check_website(url, username)
        if status_code == 200:
            print(f"\033[1;92m Found!\033[0m {url.format(username)}")
            with open(f"{username}.txt", "a") as file:
                file.write(f"{url.format(username)}\n")
        elif status_code is None:
            print(f"\033[1;91mError occurred while checking {site}\033[0m")
        else:
            print(f"\033[1;93mNot Found!\033[0m")

if __name__ == "__main__":
    banner()
    scanner()
