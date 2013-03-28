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
Module: MovieList.MovieEditDialog
Created on: 28 Mar 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

from gi.repository import Gtk, Gdk
from constants import DIALOG_BUILD_FILE
from Movie import Movie


# test data
testMovie = Movie(title='This Is A Test Movie',
                  date=2000,
                  director='Bob Bowles',
                  duration=100,
                  stars='Zhang Dehua; Bob Bowles; Mum',
                  genre='Domestic Drama',
                  media='avi',
                  )
print(testMovie)
defaultMovie = Movie(title='', date=2000, director='', duration=60,
                     stars='; delimited list',
                     genre='; delimited list',
                     media='; delimited list',
                     )
print(defaultMovie)



class MovieEditDialog(object):
    """
    Dialog for adding or editing a Movie object.
    """


    def __init__(self, movie=defaultMovie):
        """
        Construct and run the dialog
        """

        self.builder = Gtk.Builder()
        self.builder.add_from_file(DIALOG_BUILD_FILE)
        self.builder.connect_signals(self)

        # other ui setup goes here
        self.movie = movie

        # get a reference to the main window itself and display the window
        self.dialog = self.builder.get_object('movieEditDialog')

        # get the dialog editable areas
        self.titleEntry = self.builder.get_object('titleEntry')
        self.dateSpinbutton = self.builder.get_object('dateSpinbutton')
        self.directorEntry = self.builder.get_object('directorEntry')
        self.durationSpinbutton = self.builder.get_object('durationSpinbutton')
        self.starsEntry = self.builder.get_object('starsEntry')
        self.genreEntry = self.builder.get_object('genreEntry')
        self.mediaEntry = self.builder.get_object('mediaEntry')

        # populate the dialog fields
        self.titleEntry.set_text(self.movie.title)
        self.dateSpinbutton.set_text(str(self.movie.date))
        self.directorEntry.set_text(self.movie.director)
        self.durationSpinbutton.set_text(str(self.movie.duration))
        self.starsEntry.set_text(self.movie.stars)
        self.genreEntry.set_text(self.movie.genre)
        self.mediaEntry.set_text(self.movie.media)


    def run(self):
        """
        Display the edit dialog and return any changes.
        """

        self.dialog.show()
        response = self.dialog.run()

        # if the ok button was pressed update the movie object
        if response == Gtk.ResponseType.OK:
            self.movie.title = self.titleEntry.get_text()
            self.movie.date = int(self.dateSpinbutton.get_text())
            self.movie.director = self.directorEntry.get_text()
            self.movie.duration = int(self.durationSpinbutton.get_text())
            self.movie.stars = self.starsEntry.get_text()
            self.movie.genre = self.genreEntry.get_text()
            self.movie.media = self.mediaEntry.get_text()

        self.dialog.destroy()

        return response, self.movie



    # TODO: other action(s) go here




if __name__ == '__main__':

    app = MovieEditDialog()
    response, movie = app.run()
    print(movie)
