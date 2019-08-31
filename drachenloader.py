#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pytube
import urllib.request
import os.path
import datetime
from termcolor import colored
from bs4 import BeautifulSoup

#checks progress of the download
def check_progress(
    stream=None,
    chunk=None,
    file_handle=None,
    remaining=None,
    ):
    percent = 100 * (file_size - remaining) / file_size
    print (colored('{:00.0f}% downloaded'.format(percent), 'green'), end="\r")

#sets up a directory based on the current date
def setDirectory():
    global direc, urlfile
    date = datetime.datetime.now()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%y")
    direc = day+'.'+month+'.'+year
    if os.path.isdir(direc)==False:
        os.mkdir(direc)

def urlExistsInFile(url=None):
    if os.path.exists('urls.txt'):
        with open('urls.txt') as f:
            if url in f.read():
                return True
            else:
                return False
    else: 
        return False

def addUrlToFile(url=None):
    f= open("urls.txt","a+")
    f.write(url+' ')
    f.close

#get the urls of all videos from the first search page of youtube
#initiates the download of each video
def get_urls(word=None):
    query = urllib.parse.quote(word)
    url = 'https://www.youtube.com/results?search_query=' + query + '&sp=EgIIAg%253D%253D'
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        url = 'https://www.youtube.com' + vid['href']
        if urlExistsInFile(url)==False:
            download_video(url, direc)
            addUrlToFile(url)
        else:
            print()
            print(colored(url + ' - Video berreits gedownloaded', 'green'))
            
#downloads youtube video which is specified by an url
def download_video(url=None, directory=None):
    try:
        global video, title, video_type, file_size, file_size_human

        #the youtube object
        video = pytube.YouTube(url, on_progress_callback=check_progress)

        #title of the video
        title  = (video.title[:40] + '..') if len(video.title) > 40 else video.title

        #download video in top quality if video size is lower than 50MB
        if video.streams.filter(progressive=True).asc().first().filesize > 50000000:
            video_type = video.streams.filter(progressive=True).desc().first()
        else: 
            video_type = video.streams.filter(progressive=True).asc().first()

        #get file size and make it readable for humans
        file_size = video_type.filesize
        file_size_human = file_size/1000000

        print()
        print (colored("Downloading --> "+title, 'yellow'))
        print (colored(str(round(file_size_human, 1))+'MB', 'yellow'))
        #download the video
        video_type.download(directory)
        print(colored('DONE                ', 'green'), end="\r")
        print()

    #catch all possible exceptions
    except pytube.exceptions.LiveStreamError:
        print()
        print (colored('Livestream kann nicht geladen werden', 'red'))
    except pytube.exceptions.VideoUnavailable:
        print()
        print (colored('Video nicht verfuegbar', 'red'))
    except urllib.error.HTTPError:
        print()
        print (colored('urllib: HTTPError', 'red'))

def enter_video_url():
    print()
    url = input('Enter video url: ')
    download_video(url, '.')
    enter_video_url()


def start():
    setDirectory()
    print()
    print(colored('-<drachenloader.py v1.0>-', 'cyan'))
    print(colored('1: Download Drachenlord Fideos der letzten 24 Stunden', 'cyan'))
    print(colored('2: Download video by URL', 'cyan'))
    print(colored('3: Download playlist by URL', 'cyan'))
    print(colored('Beenden mit ctrl+c', 'cyan'))
    a = input('Eingabe: ')
    if a == '1':
        get_urls("Drachenlord")
    if a == '2':
        enter_video_url()

begin = start()

			
