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
import datetime


# test data
testMovie = Movie(title='This Is A Test Movie',
                  date=2000,
                  director='Bob Bowles',
                  duration=100,
                  stars='Zhang Dehua; Bob Bowles; Mum',
                  genre='Domestic Drama',
                  media='avi',
                  )
defaultMovie = Movie(title='TEST', date=2000, director='', duration=60,
                     stars='; delimited list',
                     genre='; delimited list',
                     media='; delimited list',
                     )



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

        # adjust the date spinbutton range for the current year
        now = datetime.datetime.now()
        self.dateSpinbutton.set_range(1900, now.year)

        # populate the dialog fields
        self.titleEntry.set_text(movie.title)
        self.dateSpinbutton.set_value(movie.date)
        self.directorEntry.set_text(movie.director)
        self.durationSpinbutton.set_value(movie.duration)
        self.starsEntry.set_text(movie.stars)
        self.genreEntry.set_text(movie.genre)
        self.mediaEntry.set_text(movie.media)


    def run(self):
        """
        Display the edit dialog and return any changes.
        """

        # self.dialog.show()
        response = self.dialog.run()
        movie = None

        # if the ok button was pressed update the movie object
        if response == Gtk.ResponseType.OK:
            movie = Movie(title=self.titleEntry.get_text(),
                          date=self.dateSpinbutton.get_value_as_int(),
                          director=self.directorEntry.get_text(),
                          duration=self.durationSpinbutton.get_value_as_int(),
                          stars=self.starsEntry.get_text(),
                          genre=self.genreEntry.get_text(),
                          media=self.mediaEntry.get_text(),
                          )
            print(movie)
        else:
            movie = Movie()

        self.dialog.destroy()

        return response, movie



if __name__ == '__main__':

    app = MovieEditDialog()
    response, movie = app.run()
    print(movie)
