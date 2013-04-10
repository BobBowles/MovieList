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
Module: MovieList.MovieListIO
Created on: 1 Apr 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

import io
import pickle
from Movie import Movie



class MovieListIO(object):
    """
    This module is responsible for saving and loading movie data in the
    MovieList to disk.
    At time of initial writing this may not need to be very complicated.
    However, it is expected that later more than one data format will be
    supported, and it seemed wise to delegate all i/o to a dedicated module to
    avoid cluttering up the main application.
    """


    def __init__(self, movieList=None):
        """
        Initialize the reference to the parent so we can access the necessary
        data.
        """

        self.movieList = movieList


    def save(self):
        """
        Save the data to disk.
        """

        # TODO: extract the data from the movieListStore
        outputList = []
        # for row in self.movieList.movieListStore:
        for row in self.movieList.movieTreeStore:
            outputList.append(Movie.fromList(row))

        # pickle the data
        fileHandler = io.open(self.movieList.getFileName(), 'wb')
        pickle.dump(outputList, fileHandler)
        fileHandler.close()


    def load(self):
        """
        Load the data from disk.
        """

        # load in the data  from the pickle file
        fileHandler = io.open(self.movieList.getFileName(), 'rb')
        inputList = pickle.load(fileHandler)
        fileHandler.close()

        # load the data into the movieListStore
        self.movieList.movieTreeStore.clear()
        self.populateMovieTreeStore(inputList)


    def populateMovieTreeStore(self, movieList):
        """
        Utility for populating the treeStore from a stored list of movies.
        """

        for movie in movieList:
            self.appendMovie(movie)


    def appendMovie(self, movie):
        """
        Append a movie to the treeStore.

        Find any parent series, then append the movie.
        """

        # TODO: this is sooo kludgy - work out the parent iteration
        movieTreeStore = self.movieList.movieTreeStore

        seriesIter = None
        try:
            if movie.series:
                # find the 'movie' that is the series name
                movieIter = movieTreeStore.get_iter_first()
                while movieIter:
                    if movie.series == movieTreeStore[movieIter][0]:
                        seriesIter = movieIter
                        break
                    movieIter = movieTreeStore.iter_next(movieIter)
        except AttributeError as a:
            pass

        self.movieList.movieTreeStore.append(seriesIter, movie.toList())


    def importCsv(self):
        """
        Import CSV data.

        The assumed format for the csv data lines is as follows:
        title,date,director,duration,genre,stars,other_stuff_can_be_ignored

        NOTE: No attempt is made to preserve information about media or series.
        """

        fileHandler = io.open(self.movieList.getFileName(), 'rt')

        # get the data and add it to the list store.
        self.movieList.movieListStore.clear()
        while True:
            data = fileHandler.readline()
            if not data:
                break
            dataList = data[:-1].split(',')
            movie = Movie(
                          title=dataList[0],
                          date=(int(dataList[1]) if dataList[1].isnumeric()
                                else 1900),
                          director=dataList[2],
                          duration=(int(dataList[3]) if dataList[3].isnumeric()
                                    else 0),
                          genre=dataList[4],
                          stars=dataList[5],
                          )
            self.movieList.movieListStore.append(movie.toList())
        fileHandler.close()
