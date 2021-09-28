"""Common constants for formatting."""
FILE_LINE_BREAK = '\n'
FILE_TAB = '  '
FILE_SEPARATOR = '---'
FILE_LOWRES_MAXSIZE = 4800000
LINK_SEPARATOR = ' | '
LINK_COMMA = ', '
HTML_LINE_BREAK = '<br/>\n'
HTML_TAB = '&nbsp&nbsp'
HTML_SEPARATOR = '<hr/>'
# PUNCTUATION = ":,.?!/\\-_\{\}'"
PUNCTUATION = ':,.?!/\\-_\{\}\''
QUOTE_CHARACTERS = '“”'
FACEBOOK = 'https://facebook.com/%s'
LINKEDIN = 'https://linkedin.com/in/%s'
SLIDESHARE_USERNAME = 'duruofei/'

SCHOLAR = 'https://scholar.google.com/citations?user=%s'
SCHOLAR_PHOTO_URL = 'https://scholar.google.com/citations?view_op=view_photo&user=%s'
SCHOLAR_PHOTO_LOCAL = 'photos/%s_s.jpg'
WEBSITE_PHOTO_LOCAL = 'photos/%s_w.jpg'
LINKEDIN_PHOTO_LOCAL = 'photos/%s_l.jpg'
TWITTER_PHOTO_LOCAL = 'photos/%s_t.jpg'
FACEBOOK_PHOTO_LOCAL = 'photos/%s_f.jpg'
SELECTED_PHOTO_LOCAL = 'photos/%s.jpg'

TWITTER = 'https://twitter.com/%s'
VIMEO = 'https://vimeo.com/%s'
INSTAGRAM = 'https://www.instagram.com/%s'
GITHUB = 'https://github.com/%s'
YOUTUBE = 'https://youtube.com/channel/%s'
RESEARCH_GATE = 'https://researchgate.net/profile/%s'
MAILTO = 'mailto:%s'
GOOGLE_SEARCH = 'https://google.com/search?q=%s'

CSS_HTML = '<link rel="stylesheet" href="/%s" />'
JS_HTML = '<script src="/%s"></script>'
DEBUG_HTML_SCRIPT = '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" crossorigin="anonymous"><link rel="stylesheet" href="debug.css"><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script><script src="debug.js"></script>'
YOUTUBE_IFRAME = '<div class="video-container"><iframe class="video-player" src="https://youtube.com/embed/%s?showinfo=0&iv_load_policy=3" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div>'
VIMEO_IFRAME = '<div class="video-container"><iframe src="https://player.vimeo.com/video/%s" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div>'
MP4_IFRAME = '<div class="video-container"><video controls><source src="%s.mp4" type="video/mp4">Your browser does not support the video tag.</video></div>'
PAPERS_IN_PROJECT = '<!-- publication: papers/data_pub_single_column.html | visible=1,project>>%s -->'
TALKS_IN_PROJECT = '<div class="box alt"><div class="row 50%% uniform">\n<!-- talks: talks/data_talks_3cols.html | visible=1,project>>%s -->\n</div></div>'
VIDEOS_IN_PROJECT = '<div class="box alt"><div class="row 50%% uniform">\n<!-- videos: videos/data_videos_3cols.html | visible=1,project>>%s -->\n</div></div>'
CITES_IN_PROJECT = '<ul><!-- references: cites/data_cites_list.html | visible=1,cited_project>>%s --></ul>\n'
CITED_BY_IN_PROJECT = '<ul><!-- references: cites/data_cites_list.html | visible=1,cites_project>>%s --></ul>\n'
RELATED_IN_PROJECT = '<ul><!-- references: cites/data_cites_list.html | visible=1,related_project>>%s --></ul>\n'
RELATED_WORK_IN_PROJECT = '<ul><!-- references: cites/data_cites_list.html | visible=1,related_project>>%s --></ul>\n'
FOLLOWUP_IN_PROJECT = '<ul>\n<!-- references: cites/data_cites_list.html | visible=1,followup_projects>>%s -->\n</ul>'
AWARD_HTML = '<span class="award">%s</span>'

TO_APPEAR = '<i>to appear</i>'
YOUTUBE_VIDEO_URI = 'https://youtu.be/%s'
VIMEO_VIDEO_URI = 'https://vimeo.com/%s'

# Common keys in bibTeX. Used in the Paper class.
BIB_ITEMS = [
    'b_title', 'b_author', 'journal', 'booktitle', 'school', 'institution',
    'note', 'year', 'volume', 'number', 'editor', 'location', 'publisher',
    'b_month', 'day', 'b_pages', 'b_numpages', 'series', 'doi'
]

# Maps type to a bibTeX book.
PAPER_BTYPE2BIB_BOOK = {
    'article': 'journal',
    'incollection': 'incollection',
    'inproceedings': 'booktitle',
    'conference': 'booktitle',
    'techreport': 'institution',
    'phdthesis': 'school',
    'masterthesis': 'school',
    'bachelorthesis': 'school',
    'misc': 'howpublished'
}

# Maps type to a sorting number.
PAPER_TYPE2BIB_NUM = {
    'conf': 15,
    'inproceedings': 15,
    'incollection': 15,
    'poster': 5,
    'lbw': 10,
    'workshop': 12,
    'demo': 6,
    'article': 20,
    'journal': 20,
    'phdthesis': 18,
    'phd': 18,
    'ms': 14,
    'bs': 9,
    'patent': 13,
    'misc': 1,
    'arxiv': 12,
    'report': 1,
    'techreport': 1,
}

# Maps type to a bibTeX type.
PAPER_TYPE2BIB_TYPE = {
    'inproceedings': 'inproceedings',
    'incollection': 'incollection',
    'conf': 'inproceedings',
    'poster': 'inproceedings',
    'lbw': 'inproceedings',
    'workshop': 'inproceedings',
    'demo': 'inproceedings',
    'article': 'article',
    'journal': 'article',
    'phdthesis': 'phdthesis',
    'phd': 'phdthesis',
    'masterthesis': 'masterthesis',
    'ms': 'masterthesis',
    'bachelorthesis': 'bachelorthesis',
    'bs': 'bachelorthesis',
    'misc': 'misc',
    'patent': 'misc',
    'arxiv': 'misc',
    'techreport': 'techreport',
    'report': 'techreport',
}
