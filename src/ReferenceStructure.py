# https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management
BibTeXTypes = set(['article', 'book', 'booklet', 'conference', 'inbook',
                   'incollection', 'inproceedings', 'manual', 'mastersthesis',
                   'misc', 'phdthesis', 'proceedings', 'techreport',
                   'unpublished'])

# Some fields will only be used for certain type of references,
#    some will be used differently for different types.
# May consider use several database tables or json type in the future.
DatabaseReferenceStructure = ['ID', 'Title', 'Authors', 'Type', 'PubIn',
                              'Year', 'Labels', 'AddedTime']

# ID: Reference ID in database
# Title: Title of reference item
# Author: Authors of the reference item
# Type: BibTexTypes, article, book, misc, ...
# PubIn: name of journal, conference, or howpublished

# Year: year published.
# Label: user added labels.
# AddedTime: reference item added time.
# Note: user note
# Publisher: publisher.

# Volume: Volume of journal article, or book.
# Number: issue number for journal articles or used for other cases.
# Pages: pages of article or part of a book.
# Month: month of journal.
# Abstract: abstract of papers.

# Booktitle: unknown.
# Chapter:
# Edition:
# Isbn:
# Issn:

# Series:
# Address:
# Organization:
# Doi:
# Keywords:

# Other1:
# Other2:
# Other3:
# Other4:
# Other5:

ExtendedDatabaseReferenceStructure = ['ID', 'Title', 'Author', 'Type', 'PubIn',
                              'Year', 'Label', 'AddedTime', 'Note', 'Publisher'
                              'Volume', 'Number', 'Pages', 'Month', 'Abstract',
                              'Booktitle', 'Chapter', 'Edition', 'Isbn', 'Issn',
                              'Series', 'Address', 'Organization', 'Doi', 'Keywords',
                              'Other1', 'Other2', 'Other3', 'Other4', 'Other5']

DB_BaseFields = ['ID', 'RefAbsID', 'Labels', 'AddedTime', 'Citekey', 'Flags', 'Attachments', 'Links']

DB_ArticleFields = ["author", "title", "journal", "year",
                    "volume", "number", "pages", "month", "note",
                    "abstract"]

DB_BookFields = ["author", "title", "publisher", "year",
                 "volume", "number", "series", "address", "edition", "month", "note",
                 "isbn"]

DB_BookletFields = ["title",
                    "author", "howpublished", "address", "month", "year", "note"]

DB_ConferenceFields = ["author", "title", "booktitle", "year",
                       "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note",
                       "conference", "abstract"]

DB_InbookFields = ["author", "editor", "title", "chapter", "pages", "publisher", "year",
                   "volume", "number", "series", "type", "address", "edition", "month", "note"]

DB_IncollectionFields = ["author", "title", "booktitle", "publisher", "year",
                         "editor", "volume", "number", "series", "type", "chapter", "pages", "address", "edition", "month", "note"]

DB_InproceedingsFields = ["author", "title", "booktitle", "year",
                          "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note",
                          "conference", "abstract"]

DB_ManualFields = ["title",
                   "author", "organization", "address", "edition",
                   "month", "year", "note"]

DB_MastersthesisFields = ["author", "title", "school", "year",
                          "type", "address", "month", "note"]

DB_MiscFields = ["author", "title", "howpublished", "month", "year", "note"]

DB_PhdthesisFields = ["author", "title", "school", "year",
                      "address", "month", "keywords", "note"]

DB_ProceedingsFields = ["title", "year",
                        "editor", "volume", "number", "series", "address", "month", "organization", "publisher", "note",
                        "author"]

DB_TechreportFields = ["author", "title", "institution", "year",
                       "type", "number", "address", "month", "note"]

DB_UnpublishedFields = ["author", "title", "note",
                        "month", "year"]

DB_ExtendFields = ['E1', 'E2', 'E3', 'E4', 'E5']

DatabaseStandardStructure = {'Article':         DB_ArticleFields,
                             'Book':            DB_BookFields,
                             'Booklet':         DB_BookletFields,
                             'Conference':      DB_ConferenceFields,
                             'Inbook':          DB_InbookFields,
                             'Incollection':    DB_IncollectionFields,
                             'Inproceedings':   DB_InproceedingsFields,
                             'Manual':          DB_ManualFields,
                             'Mastersthesis':   DB_MastersthesisFields,
                             'Misc':            DB_MiscFields,
                             'Phdthesis':       DB_PhdthesisFields,
                             'Proceedings':     DB_ProceedingsFields,
                             'Techreport':      DB_TechreportFields,
                             'Unpublished':     DB_UnpublishedFields
                             }

DB_TypeCode ={'Article':         10,
              'Book':            11,
              'Booklet':         12,
              'Conference':      13,
              'Inbook':          14,
              'Incollection':    15,
              'Inproceedings':   16,
              'Manual':          17,
              'Mastersthesis':   18,
              'Misc':            19,
              'Phdthesis':       20,
              'Proceedings':     21,
              'Techreport':      22,
              'Unpublished':     23
             }

AllFieldSet = set(["author", "title", "journal", "year", "number", "pages",
                   "month", "note", "abstract", "volume", "isbn", "issn",
                   "series", "edition", "address", "publisher", "booktitle",
                   "chapter", "conference", "howpublished", "organization"])

# https://verbosus.com/bibtex-style-examples.html
# http://web.mit.edu/rsi/www/pdfs/bibtex-format.pdf
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node6.html
# http://newton.ex.ac.uk/tex/pack/bibtex/btxdoc/node7.html

# Example: XXXFieldSet = set([ #Required Fields
#                              #Optional Fields
#                              #Controvertible Fields ])

ArticleFieldSet = set(["author", "title", "journal", "year",
                       "volume", "number", "pages", "month", "note",
                       "abstract"])

BookFieldSet = set(["author", "title", "publisher", "year",
                    "volume", "number", "series", "address", "edition", "month", "note",
                    "isbn"])

BookletFieldSet = set(["title",
                       "author", "howpublished", "address", "month", "year", "note"])

ConferenceFieldSet = set(["author", "title", "booktitle", "year",
                          "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note",
                          "conference", "abstract"])

InbookFieldSet = set(["author", "editor", "title", "chapter", "pages", "publisher", "year",
                      "volume", "number", "series", "type", "address", "edition", "month", "note"])

IncollectionFieldSet = set(["author", "title", "booktitle", "publisher", "year",
                            "editor", "volume", "number", "series", "type", "chapter", "pages", "address", "edition", "month", "note"])

InproceedingsFieldSet = set(["author", "title", "booktitle", "year",
                             "editor", "volume", "number", "series", "pages", "address", "month", "organization", "publisher", "note",
                             "conference", "abstract"])

ManualFieldSet = set(["title",
                      "author", "organization", "address", "edition",
                      "month", "year", "note"])

MastersthesisFieldSet = set(["author", "title", "school", "year",
                             "type", "address", "month", "note"])

MiscFieldSet = set([
                    "author", "title", "howpublished", "month", "year", "note"])

PhdthesisFieldSet = set(["author", "title", "school", "year",
                         "address", "month", "keywords", "note"])

ProceedingsFieldSet = set(["title", "year",
                           "editor", "volume", "number", "series", "address", "month", "organization", "publisher", "note",
                           "author"])

TechreportFieldSet = set(["author", "title", "institution", "year",
                          "type", "number", "address", "month", "note"])

UnpublishedFieldSet = set(["author", "title", "note",
                           "month", "year"])

ReferenceStandardStructure = {'article':         ArticleFieldSet,
                              'book':            BookFieldSet,
                              'booklet':         BookletFieldSet,
                              'conference':      ConferenceFieldSet,
                              'inbook':          InbookFieldSet,
                              'incollection':    IncollectionFieldSet,
                              'inproceedings':   InproceedingsFieldSet,
                              'manual':          ManualFieldSet,
                              'mastersthesis':   MastersthesisFieldSet,
                              'misc':            MiscFieldSet,
                              'phdthesis':       PhdthesisFieldSet,
                              'proceedings':     ProceedingsFieldSet,
                              'techreport':      TechreportFieldSet,
                              'unpublished':     UnpublishedFieldSet
                             }
