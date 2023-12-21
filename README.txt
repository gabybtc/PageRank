This was an extra credit project for a UMass Search Engines course.

src/ is a folder that contains the source code.
inlinks.txt - A text file with the top 100 pages by number of inlinks within the links.srt.gz file, with the page title (URL), rank (1..100), and inlink count on each line in that order. The three data items are separated with whitespace characters.
pagerank.txt - a text file with the top 100 pages within links.srt.gz sorted by their PageRank, with page title (URL), rank (1..100) and PageRank score on each line. The three data items are separated with whitespaces.

The big file used to test the pagerank algorithm (links.srt.gz) can be found at https://drive.google.com/file/d/1shc3mjEGK9hI99tY27eX_OasM7boc5ne/view
To run: use terminal command lines
For pageRank algorithm until convergence: "python3 pagerank.py links.srt.gz 0.20 0.005 inlinks.txt pagerank.txt 100"
For running pageRank algorithm exactly twice: "python3 pagerank.py links.srt.gz 0.20 "exactly 2" inlinks.txt pagerank.txt 100"

pagerank.py's algorithm run on links.srt.gz (to conversion) runtime is 16 seconds
