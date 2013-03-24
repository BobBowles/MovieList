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
Module: MovieList.MovieList
Created on: 24 Mar 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

# Copyright (C) 2012 Bob Bowles <bobjohnbowles@gmail.com>
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

from gi.repository import Gtk, Gdk
from constants import UI_BUILD_FILE, UI_CSS_FILE



class MovieList:
    """
    The MovieList object
    """


    def __init__(self):
        """
        Load the UI elements from the .glade file.
        """

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_BUILD_FILE)
        self.builder.connect_signals(self)

        # TODO: other setup stuff goes here

        # get a reference to the main window itself and display the window
        self.window = self.builder.get_object('window')
        self.window.show_all()


    # TODO: other action(s) go here


    def on_window_destroy(self, widget):
        """
        Handler for closing window. A quick clean kill of the entire app.
        """

        Gtk.main_quit()



# # configure themed styles for the grid buttons
# cssProvider = Gtk.CssProvider()
# cssProvider.load_from_path(UI_CSS_FILE)
# screen = Gdk.Screen.get_default()
# styleContext = Gtk.StyleContext()
# styleContext.add_provider_for_screen(screen, cssProvider,
#                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

app = MovieList()
Gtk.main()
