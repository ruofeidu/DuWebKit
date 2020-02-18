# DuWebKit

DuWebkit is a minimized subset of Ruofei Du's Python toolkits of personal website. It compiles minimized HTML, JS, and CSS by parsing data from a Google
Sheet database.

## Motivation

The motivation is: given a set of papers with different authors, I have to
manually generate BibTeX items, links to individual's website, and write
template for each paper. It's tedious to maintain all links up-to-update so I
need a structured way to do so. What if we can maintain all the data in two or
more Google Sheet?

Why not ``SQL``? PHPMYADMIN is insecure to play with while adding new rows
require significant amount of efforts to log-in, ensure data integrity, and
complex IO.

Why not ``JSON``? In 2018, I made VarshneyWebsite, which uses JSON for storing
students and papers. However, JSON file is hard to search and find, and column
names are repetative.

Why ``gSheets`` is a better choice for personal website? In 2019, I started to
build a new toolchain to leverage Google Sheets for updating such small-scale
relational database. It offers me a convenient interface to have a quick
overview of all of my previous submissions and coauthors.

You may need a developer account and access
[this sample Google sheet](https://docs.google.com/spreadsheets/d/1JyYNAQz2OLK3p8f0JGhQvHjr8p-jA8bOo2z2Mm3Px4I/edit?usp=sharing)
for a template Google sheet to compile a website from this set of Python
scripts. This is the opensourced version of my private repository and may not
reflected what I am showing on <http://duruofei.com.> Please feel free to pull
request or ask me for anything.

## Dependencies

Use pip3 install -r requirements.txt, or:

```bash
pip3 install --upgrade pip
pip3 install configparser
pip3 install --upgrade httplib2 oauth2client
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install --upgrade markdown htmlmin
pip3 install --upgrade selenium
pip3 install --upgrade beautifulsoup4
pip3 install --upgrade csscompressor
pip3 install --upgrade jsmin
```

## Build

Simply run:

```bash
python3 build.py
```

The results will be written into ``builds/`` folder by default.

I am not checking in my photos, but the images should be located in the
``builds/images`` folder.

## Template Grammar

See ``scripts/utils/regex.py`` for the complete grammar and feel free to extend
it.

### include

```html
<!-- include: header.html -->
```

### css, js

```html
<!-- css: main.css -->
```

## TODO list

* Multiple language support.
* Better CSS for the demo project.
* The sample HTML has typos and unmatched tags. I suggested you write your own :)

## License

DuWebKit Creative Commons Attribution-NonCommercial-ShareAlike 3.0
License with 996 ICU clause: [![996.ICU](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu/#/en_US)

The above license is only granted to entities that act in concordance with local labor laws. In addition, the following requirements must be observed:

- The licensee must not, explicitly or implicitly, request or schedule their employees to work more than 45 hours in any single week.
- The licensee must not, explicitly or implicitly, request or schedule their employees to be at work consecutively for 10 hours.

Please refer to individual GLSL files (.glsl) for License of Third-Party Shaders.
