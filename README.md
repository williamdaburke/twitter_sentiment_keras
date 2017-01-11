#If you like this challenge, you will like working with Black Swan's Data Science team!

First, before delving into the challenges, we would like to explain that we use version control and virtual environments in our work. We think they are essential to produce good quality stuff and it helps us a lot! So we expect you do the same whlist working on these challenges. Please commit several times as your work progress with meaningful comments and create a requirements file so we can see what you are working with.

Your end result should be scripts (suitably commented) written in Python (2 or 3) that anyone can easily run. The way you organise them it's up to you.
 
Now, as for the challenges, you find the data you need in the "data" folder and should be comprised of 3 files: csv_file.csv, json_file.json, txt_file.txt

The challenges are divided into 4 parts:

__API Access__

This challenge will involve querying an API and extracting information from it. The API in question provides information on Game of Thrones, allowing one to access information on the houses, characters and books.

* API URL: http://anapioficeandfire.com/api/{SECTION}/{INDEX}

Where SECTION can be either ‘books’, ‘characters’, or ‘houses’ and INDEX is an integer to a certain entry in a section.

For example, to access the character Peter Baelish, the full request would be http://anapioficeandfire.com/api/characters/823, where 823 is the index corresponding to that character. 

We would like you to answer the following:

  a) What index corresponds to the house “House Breakstone”?
 
  b) How many males, females and unknown genders are there in the first 40 characters? Note, index 0 does not correspond to a character, so full range is 1 - 40 both ends inclusive. 

  c) How many books can be accessed from this API?

  d) How many books does the character ‘High Septon’ appear in? (ignoring ‘povcharacters’) 

Hint: index value of Septon needs to be found first; it is smaller than 20.

* Download and install [miniconda](http://conda.pydata.org/miniconda.html) or anaconda

* Create a virtual environment (NOTE: python 3!)
  
  ```
  $ conda create -n miniconometrics python=3 --file requirements_conda.txt
  ```

__Configure__

  The configuration highly depends on the available master input data, modify config.py
  to make miniconometrics understand its contents. config.py is meant to be self explanatory.

__Run__

* activate the environment