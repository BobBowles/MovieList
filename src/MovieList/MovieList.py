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
from Movie import Movie
from MovieEditDialog import MovieEditDialog


# test data
testMovie = Movie(title='This Is A Test Movie',
                  date=2000,
                  director='Bob Bowles',
                  duration=100,
                  stars='Zhang Dehua; Bob Bowles; Mum',
                  genre='Domestic Drama',
                  media='avi',)
print(testMovie)


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

        # references to the widgets we need to manipulate
        self.movieListStore = self.builder.get_object('movieListStore')
        self.movieTreeView = self.builder.get_object('movieTreeView')
        self.movieTreeSelection = self.builder.get_object('movieTreeSelection')
        self.statusbar = self.builder.get_object('statusbar')

        # TODO: this is a test data display
        self.movieListStore.append(testMovie.toList())

        # get a reference to the main window itself and display the window
        self.window = self.builder.get_object('window')
        self.window.show_all()


    # TODO: other action(s) go here


    # TODO: File menu actions

    def on_fileQuitImageMenuItem_activate(self, widget):
        """
        Handler for quitting the app from the file menu.

        This implementation just passes on responsibility to on_window_destroy().
        """

        self.on_window_destroy(widget)


    # TODO: Edit menu actions

    def on_addMovieButton_clicked(self, widget):
        """
        Handler for the toolbar add button.

        Displays a new empty movie in the edit dialog. If the movie information
        is changed, add the movie information to the list.
        """

        # an empty movie object to fill in
        movie = Movie()

        # the statusbar context
        context = self.statusbar.get_context_id('add')

        # invoke the dialog
        dialog = MovieEditDialog(parent=self.window, movie=movie)
        response, newMovie = dialog.run()

        # update the model and display
        if (response == Gtk.ResponseType.OK and newMovie != movie):
            self.movieListStore.append(newMovie.toList())
            self.statusbar.push(context,
                                'Added: {} ({})'.format(newMovie.title,
                                                        newMovie.date))
        else:
            self.statusbar.push(context, 'Add New Movie aborted')


    def on_editMovieButton_clicked(self, widget):
        """
        Handler for the toolbar edit button.

        Takes the current selected movie and displays it in the edit dialog. If
        the movie information is changed, update the movie information in the
        list.
        """

        # get the current movie selection
        treeModel, treeIndex = self.movieTreeSelection.get_selected()
        movie = Movie.fromList(treeModel[treeIndex])

        # context of statusbar messages
        context = self.statusbar.get_context_id('edit')

        # invoke the dialog
        dialog = MovieEditDialog(parent=self.window, movie=movie)
        response, editedMovie = dialog.run()

        # update the model and display
        if (response == Gtk.ResponseType.OK and editedMovie != movie):
            movieData = editedMovie.toList()
            for col, data in enumerate(movieData):
                self.movieListStore.set_value(treeIndex, col, data)
            self.statusbar.push(context,
                                'Edited: {} ({})'.format(editedMovie.title,
                                                         editedMovie.date))
        else:
            self.statusbar.push(context, 'Edit Movie aborted')


    def on_deleteMovieButton_clicked(self, widget):
        """
        Handler for the toolbar delete button.

        Delete the currently selected movie. Confirmation is required.
        """

        # get the current movie selection
        treeModel, treeIndex = self.movieTreeSelection.get_selected()
        movie = Movie.fromList(treeModel[treeIndex])

        # context of statusbar messages
        context = self.statusbar.get_context_id('delete')

        # invoke the confirmation dialog
        dialog = Gtk.MessageDialog(self.window,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   'Confirm delete of movie {} ({})'
                                   .format(movie.title, movie.date),
                                   )
        response = dialog.run()

        # check the response
        if response == Gtk.ResponseType.OK:
            self.movieListStore.remove(treeIndex)
            self.statusbar.push(context,
                                'Deleted: {} ({})'.format(movie.title,
                                                          movie.date))
        else:
            self.statusbar.push(context, 'Delete Movie aborted')
        dialog.destroy()





    # TODO: Help menu actions


    # main window event(s)

    def on_window_destroy(self, widget):
        """
        Handler for closing window.

        A quick clean kill of the entire app.
        """

        # TODO: need to save any changes first.
        print('Destroying main window')
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
