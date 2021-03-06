#!/usr/bin/python
import sys
from sys import argv
import optparse
from os import system
import requests

key = "1e940957819058fe3ec7c59d43c09504b400110db7faa0509"
tkey = "e415520c671c26518df498d8f4736cac"
urbankey = "ub2JDDg9Iumsh1HfdO3a3HQbZi0up1qe8LkjsnWQvyVvQLFn1q"
class dict:
    def __init__(self,key,urbankey,tkey):
        self.key = key
        self.urbankey = urbankey
        self.tkey = tkey
    def getDefinition(self,word):
        definition = requests.get("http://api.wordnik.com/v4/word.json/%s/definitions?api_key=%s" % (word,self.key)).json()
        if len(definition)>=1:
            return definition[0]["text"]
        return definition
    def getHyphenation(self,word):
        hyphenation = requests.get("http://api.wordnik.com/v4/word.json/%s/hyphenation?api_key=%s" % (word,self.key)).json()
        return hyphenation
    def getAudio(self,word):
        url = requests.get("http://api.wordnik.com/v4/word.json/%s/audio?api_key=%s" % (word,self.key)).json()
        if len(url)>=1:
            url = url[0]["fileUrl"]
        else:
            return False,"",""
        return True,url,requests.get(url)
    def getUrban(self,word):
        urb = requests.get("https://mashape-community-urban-dictionary.p.mashape.com/define?term=%s"
        % word, headers={"X-Mashape-Key": self.urbankey}).json()
        if len(urb["list"])>0:
            return urb["list"][0]["definition"]
    def getThesaurus(self,word):
        response = requests.get("http://words.bighugelabs.com/api/2/%s/%s/json"
                            % (self.tkey, word)).json()
        return response



""" Returns the options that the user
defined as well as the actual argument defined"""


def get_args():
    arg = optparse.OptionParser()
    arg.add_option("-a", "--audio", action="store_true", default=False)
    arg.add_option("-t", "--thesaurus", action="store_true", default=False)
    arg.add_option("-u", "--urban", action="store_true", default=False)
    return arg.parse_args(argv)


def check_args_valid(required_args):
    if len(required_args) == 1:
        print("usage: define [options]\
        \n-a, --audio Audio pronounciations\
        \n-t, --thesaurus Thesaurus\
        \n-u, --urban, Search Urban Dictionary instead of Wordnik")
        sys.exit()


def get_wordapi_client():
    return dict(key,urbankey,tkey)


def play_definition(word, client):
    if sys.version_info > (3,):
        ask = input("\nWould you like to hear audio pronounciation? [y/N] ")
    else:
        ask = raw_input("\nWould you like to hear audio pronounciation? [y/N] ")

    if ask.lower().startswith("y"):
        valid,url,obj = client.getAudio(word)
        if valid==False:
            print("Couldn't get Audio")
            return
        # filen = wget.download(url,"/tmp")
        down = obj.content
        filen = url.split("/")[5]
        buff = open("/tmp/%s" % filen, "wb")
        buff.write(down)
        buff.close()
        system("gst-launch-1.0 playbin uri=file:///tmp/%s -q" % filen)
        while True:
            if sys.version_info > (3,):
                ask = input("\nWould you like to hear it again? [y/N] ")
            else:
                ask = raw_input("\nWould you like to hear it again? [y/N] ")
            if ask.lower().startswith("y"):
                system("gst-launch-1.0 -q playbin uri=file:///tmp/%s" % filen)
            else:
                break


def print_urban_dictionary_definition(word,client):
    urb = client.getUrban(word)
    if urb:
        print(word.upper() + ":\n" + client.getUrban(word))
    else:
        print("Couldn't get definition from urbandictionary.com")

def print_wordnik_definition(word, client):
    try:
        cons = []
        for i in client.getHyphenation(word):
            cons.append(i["text"])
        print(word.upper() + " " + "-".join(cons) + ": \n" +
              client.getDefinition(word))
    except TypeError:
        print("Not Found")
        sys.exit()


def print_thesaurus_response(word,client):
    response = client.getThesaurus(word)
    print("SYNONYMS: ")
    if "noun" in response:
        print("\nNouns: %s" % " ".join(response["noun"]["syn"]))
    if "verb" in response:
        print("Verbs: %s" % " ".join(response["verb"]["syn"]))


""" Given a list of words, this function will
write their respective definitions on the terminal."""


def print_each_definition(words, client, optional_args):
    audio = optional_args.audio
    thesaurus = optional_args.thesaurus
    urban = optional_args.urban
    for word in words[1:]:
        if urban:
            print_urban_dictionary_definition(word,client)
        else:
            print_wordnik_definition(word, client)
        if thesaurus:
            print_thesaurus_response(word,client)
        if audio:
            play_definition(word, client)
__all__=["dict","print_each_definition"]
if __name__ == "__main__":
    (optional_args, required_args) = get_args()
    check_args_valid(required_args)
    client = get_wordapi_client()
    print_each_definition(required_args, client, optional_args)
