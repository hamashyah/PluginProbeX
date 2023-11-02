import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from progressbar import ProgressBar, Percentage, Bar, ETA, RotatingMarker, FileTransferSpeed, AdaptiveETA
import pyfiglet
from termcolor import colored

def check_wordpress(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('link'):
        if 'wp-content' in link.get('href', ''):
            return True
    return False

def get_all_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    links = [link.split('#')[0] if '#' in link else link for link in links if link.startswith(('http://', 'https://'))]
    return links, url

def get_plugins(urls):
    unique_plugins = {}
    for url in urls:
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('link'):
            href = link.get('href', '')
            if '/wp-content/plugins/' in href:
                plugin_path = href.split('/wp-content/plugins/')[1].split('/')[0]
                version = href.split('?ver=')[-1] if '?ver=' in href else 'Unknown'
                unique_plugins[plugin_path] = version
    return unique_plugins

def get_emails(urls):
    emails = []
    for url in urls:
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema:
            continue
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails += re.findall(email_pattern, response.text)
    emails = list(set(emails))
    return emails

# Create a 3D ASCII art title
title = pyfiglet.figlet_format("PluginProbeX 1.0", font="doom")
print(colored(title, 'green'))

# Create a menu
while True:
    print(colored("\nMenu:", 'green'))
    print(colored("1. Check if a website is powered by WordPress", 'green'))
    print(colored("2. Get all pages of a website", 'green'))
    print(colored("3. Get plugins used by a website", 'green'))
    print(colored("4. Get emails found on a website", 'green'))
    print(colored("5. Exit", 'green'))
    choice = input(colored("Enter your choice: ", 'green'))

    if choice == "1":
        url = input(colored('Enter the URL: ', 'green'))
        if check_wordpress(url):
            print(colored('This website is powered by WordPress.', 'green'))
        else:
            print(colored('This website is not powered by WordPress.', 'green'))
    elif choice == "2":
        url = input(colored('Enter the URL: ', 'green'))
        pages, base_url = get_all_pages(url)
        urls = [base_url] + pages
        print(colored('Pages on the website:', 'green'))
        for i, page in enumerate(urls):
            print(colored(f'Page: {page}', 'green'))
    elif choice == "3":
        url = input(colored('Enter the URL: ', 'green'))
        pages, base_url = get_all_pages(url)
        urls = [base_url] + pages
        print(colored('\nPlugins used by the website:', 'green'))
        for i, (plugin, version) in enumerate(get_plugins(urls).items()):
            print(colored(f'Plugin: {plugin}, version: {version}', 'green'))
    elif choice == "4":
        url = input(colored('Enter the URL: ', 'green'))
        pages, base_url = get_all_pages(url)
        urls = [base_url] + pages
        print(colored('\nEmails found on the website:', 'green'))
        for i, email in enumerate(get_emails(urls)):
            print(colored(f'Email: {email}', 'green'))
    elif choice == "5":
        break
    else:
        print(colored("Invalid choice. Please try again.", 'red'))
