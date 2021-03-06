# Copyright (C) 2013 Bob Bowles <bobjohnbowles@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Created on 24 Mar 2013
@author: bob
"""

"""
This file just collects all the configuration constants used by the app in
one place for ease of maintenance.
"""

import os

# define the resource paths for the ui
UI_BUILD_FILE = os.path.join(os.getcwd(), 'MovieList.glade')
UI_CSS_FILE = os.path.join(os.getcwd(), 'MovieList.css')
MOVIE_DIALOG_BUILD_FILE = os.path.join(os.getcwd(), 'MovieEditDialog.glade')
SERIES_DIALOG_BUILD_FILE = os.path.join(os.getcwd(),
                                        'MovieSeriesEditDialog.glade')
IMDB_DIALOG_BUILD_FILE = os.path.join(os.getcwd(), 'IMDBDialog.glade')

# IMDB search parameters
IMDB_URI = 'http://www.imdb.com/'
IMDB_SEARCH_PREFIX = 'find?q='
IMDB_SEARCH_POSTFIX = '&s=tt&ttype=ft&ref_=fn_ft'

# xsl stylesheet for html transformation
XSL_HTML_STYLE_DOC = os.path.join(os.getcwd(), 'xml', 'MovieList2html.xsl')

# configuration file parameters
CONFIG_FILE = os.path.expanduser('~/.config/MovieList/MovieList.cfg')
FILE_SECTION = 'files'
CURRENT_FILE = 'current file'
UI_SECTION = 'ui'
WINDOW_SIZE = 'window size'
COLUMN_WIDTHS = 'column widths'
MEDIA_SECTION = 'media'
MEDIA_DIR = 'directory'
