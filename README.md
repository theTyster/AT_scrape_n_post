# This Repo

scrapes data from the Adventure Time fandom wiki and then posts that data to the fediverse.


# To run the scraper 

1. Install Python.
2. clone the git repo.
3. Open a terminal and enter the cloned directory.
4. Download the dependancies with `pip install requirements.txt`
5. While inside the directory, run `./scraper.py`. This will create a directory adjacent to the git directory with all of the scraped data.

Scraped data includes:

- Fandom wiki links to:
	- all Adventure Time Comic articles
	- thumbnails for covers and alternative covers of each comic
	- full size images of covers and alternative covers 
	- gallery of sample content from the comic
- The name of the Volume and Issue scraped
- The name of the artist (if available) who created the work

- Downloaded images of:
	- Thumbnails
	- Fullsize Images

All data is scraped into various files for different usages.
- Browsable HTML document > references origin urls
- csv > references origin urls
- JSON > references locally downloaded images
