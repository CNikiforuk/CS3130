import scrape

#Author: Carlos Nikiforuk
#Description: Demonstration of scrape as an import for a wider variety of uses.
#Date: April 24, 2015

def main():
    print("\n-----Scrape Test-----\n")
    print("This program will use scrape to download 3 pages of image thumbnails from:")
    print("http://alpha.wallhaven.cc/random\n")
    print("Each page will be downloaded and saved in its own folder in this directory.\n")

    #user input
    inp = ''
    while(inp != 'y' and inp != 'n'):
            inp = raw_input("Continue? (y/n): ")

    #create url and folder for each page, then scrape
    for i in range(1,4):
        print("\n-----Page#{}-----".format(i))
        url = "http://alpha.wallhaven.cc/random?page={}".format(i)
        folder = 'page{}'.format(i)
        scrape.scrapeFiles(url, folder, True) 

if __name__ == '__main__':
    main()
