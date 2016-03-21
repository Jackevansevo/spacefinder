# SpaceFinder App for University of Bath Integrated Project 2015-2016

The Application aims to make it easier to find study spaces on campus


# Requirements
- [Python3.5](https://www.python.org/downloads/)
- [Pip (python package manager)](http://python-packaging-user-guide.readthedocs.org/en/latest/installing/#install-pip-setuptools-and-wheel)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [NPM (Node Package Manager)](https://nodejs.org/en/)
- [Bower (Another Package Manager...)](https://www.npmjs.com/package/bower)



# Installation

## Clone the Repository

        git clone https://github.com/Jackevansevo/spacefinder.git


## Install Python Dependencies

I recommend using virtualenv, a python tool to keep dependencies required by
different projects in nice separate places. Assuming you have Python3

        pip install virtualenv

Once installed create a virtual environment for spacefinder using

        virtualenv venv

Then activate the virtual environment by running:

        source venv/bin/activate


Install Python dependencies by running

        sudo pip install -r requirements.txt


# Install Web Dependencies

Assuming you have npm and bower installed properly, install JQuery and Bootstrap
dependencies by running:

        bower install
