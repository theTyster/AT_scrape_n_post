# This Repo

scrapes data from the Adventure Time fandom wiki and then posts that data to the fediverse.


# To run the scraper 

clone the git repo, and then while inside the directory, run `./scraper`. This will create a directory adjacent to the git directory with all of the scraped data.

Scraped data includes:

- Links to:
	- all Adventure Time Comic articles
	- thumbnails for covers and alternative covers of each comic
	- full size images of covers and alternative covers 
	- gallery of sample content from the comic
- The name of the Volume and Issue scraped
- The name of the artist (if available) who created the work

All data is scraped into various files for different usages.
- Browsable HTML document
- JSON
- csv
