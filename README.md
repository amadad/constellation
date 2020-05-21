# project-constellation

A tool to accelerate competitive audits and brand discovery with machine learning by identifying actionable patterns, trends, commonalities and differentiation amongst a competitive set.

# Installation

First, you will need to install [git](https://git-scm.com/), if you don't have it already.

Next, clone this repository by opening a terminal and typing the following commands:

    $ cd $HOME  # or any other development directory you prefer
    $ git clone https://github.com/noufali/project-constellation.git
    $ cd project-constellation

## Python & Required Libraries
These files work with Python 3. So please set up a virtual environment and install the libraries listed in `requirements.txt`.

    $ pip install -r requirements.txt

word2vec.py - requires downloading vector data from the official [word2vec website](https://code.google.com/archive/p/word2vec/):  
[GoogleNews-vectors-negative300.bin.gz](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing)

topics_gensim.py (mallet method) - requires downloading the [mallet binary file](http://mallet.cs.umass.edu/dist/mallet-2.0.8.zip)
