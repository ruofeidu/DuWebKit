class Templates:
  media = '* *%s*, **[%s](%s)**, %s%s %s, %s.\n'
  students = '<div class="2u 12u$(medium) center"><span class="image fit">' \
                  '<a href="%s" target="_blank"><img src="photos/%s" alt="%s" class="face"/></a></span>' \
                  '<h4 class="center"><a href="%s" target="_blank" class="name">%s</a></h4></div>\n'

  papers = '<div class="3u 12u$(medium)"><span class="image fit">' \
                '<a href="%s" target="_blank"><img src="teaser/%s" class="pub-pic" alt="%s" /></a></span></div>' \
                '<div class="9u 12u$(medium) pub-info"><h4><a href="%s" target="_blank">%s</a></h4>' \
                '<p class="authors">%s</p>' \
                '<p class="booktitle">%s</p>' \
                '<p class="keywords">%s</p><br/><br/>' \
                '<div class="downloads">Paper: <a href="%s" target="_blank">[pdf]</a>%s%s ' \
                '%s%s%s%s%s%s%s%s | ' \
                'Cite: <a href="%s" class="bibtex">[BibTeX]</a> <a href="%s" class="bibtex">[APA]</a></div>' \
                '</p></div>'
  unpublished = '<div class="3u 12u$(medium)"><span class="image fit">' \
                     '<img src="teaser/%s" class="pub-pic" alt="%s" /></span></div>' \
                     '<div class="9u 12u$(medium) pub-info"><h4>%s</h4>' \
                     '<p class="authors">%s</p>' \
                     '<p class="booktitle">%s</p>' \
                     '<p class="keywords">%s</p><br/><br/>' \
                     '<div class="downloads">Paper: [pdf] %s%s%s | ' \
                     'Cite: <a href="%s" class="bibtex">[BibTeX]</a> <a href="%s" class="bibtex">[APA]</a></div>' \
                     '</p></div>'
