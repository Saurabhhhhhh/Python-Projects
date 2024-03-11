from pytube import YouTube

class Downloader:
    
    def __init__(self):
        print("\t\t\tWelcome to Youtube Downloader")
    
    def askUrl(self):
        self.url = input("Hey, Provide me the link of video you wanna download: ")
    
    def options(self):
        print("So here are some choices what you want to do.")
        print("1. Video: \n2. Only Audio: ")
        self.ch = input("Select one of the options: ")

    def gettingStreams(self):
        yt = YouTube(self.url)
        print(self.url)
        print("So here are some choices what you want to do.")
        print("1. Video: \n2. Only Audio: ")
        self.ch = input("Select one of the options: ")


        if self.ch == '1':
            self.streams = list(enumerate(yt.streams.filter(progressive=True)))
        elif self.ch == '2':
            self.streams = list(enumerate(yt.streams.filter(only_audio=True)))
        else:
            print("Enter from above options.")
    
    def downloading(self):
        self.choice = int(input("Enter the number corresponding to the stream you want to download: "))
        self.selected_stream = self.streams[self.choice][1]
        self.selected_stream.download()


t1 = Downloader()
t1.askUrl()
# t1.options()
t1.gettingStreams()
print(t1.ch)
for items in t1.streams:
    print(items)
t1.downloading()
