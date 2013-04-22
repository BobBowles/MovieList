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
from fileinput import filename

"""
Module: MovieList.MovieListIO
Created on: 1 Apr 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

import io
import pickle
from lxml import etree
from Movie import Movie

SAVE, LOAD = 0, 1



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

        self.ioMethods = {
                  'pickle': [self.savePickle, self.loadPickle],
                  'xml': [self.saveXml, self.loadXml]
                  }

        self.movieList = movieList


    def getFileExtension(self):
        """
        Work out what kind of file we are using.
        """

        return self.movieList.getFileName().split('.')[-1]



    def save(self):
        """
        Save the data.

        We select the appropriate save method using the filename extension as a
        key to the io methods dictionary.
        """

        self.ioMethods[self.getFileExtension()][SAVE]()


    def savePickle(self):
        """
        Save the data to disk as a pickle.
        """

        # extract the data from the movieListStore
        treeIter = self.movieList.movieTreeStore.get_iter_first()
        outputList = self.extractMovieTreeAsList(treeIter)
#        print('Output List:\n{}'.format('\n'.join('{!s}'.format(movie)
#                                                  for movie in outputList)))

        # pickle the data
        fileHandler = io.open(self.movieList.getFileName(), 'wb')
        pickle.dump(outputList, fileHandler)
        fileHandler.close()


    def saveXml(self):
        """
        Save the data in the form of an xml document.

        Iterate over the gtk treeView to create an lxml etree, then write the
        tree to a file as an xml document.
        """

        # TODO: extract the data from the gtk store into an lxml etree

        # TODO: save the tree structure as xml
        pass


    def extractMovieTreeAsList(self, treeIter):
        """
        Extract the movie data from the movieTreeStore in the form of a list.

        Recursively construct a list of the movies in the rows and child rows
        of the store.
        The base treeIter must be movieTreeStore.get_iter_first()
        """

        list = []
        while treeIter:
            list.append(Movie.fromList(self.movieList.movieTreeStore[treeIter]))
            if self.movieList.movieTreeStore.iter_has_child(treeIter):
                childIter = \
                    self.movieList.movieTreeStore.iter_children(treeIter)
                list.extend(self.extractMovieTreeAsList(childIter))
            treeIter = self.movieList.movieTreeStore.iter_next(treeIter)
        return list


    def load(self):
        """
        Load the data.

        We select and invoke the appropriate method using the file extension as
        a key to the io methods dictionary.
        """

        inputList = self\
        .ioMethods[self.getFileExtension()][LOAD](self.movieList.getFileName())

        # load the data into the movieListStore
        self.movieList.movieTreeStore.clear()
        self.populateMovieTreeStore(inputList)


    def loadPickle(self, fileName):
        """
        Load the data from a pickle file.
        """

        try:
            fileHandler = io.open(fileName, 'rb')
            return pickle.load(fileHandler)
        finally:
            fileHandler.close()


    def loadXml(self, filename):
        """
        Load the data from an xml file.

        Use lxml to parse the data, then decant the structure into the gtk
        treeStore.
        """

        # read the xml file into an lxml etree document
        doc = etree.parse(filename)

        # get the data out of the etree into a list
        root = doc.getroot()
        inputList = []
        for element in root.iterchildren():
            # print(etree.tostring(element).decode(encoding='utf-8'))

            if element.tag == 'movie':
                inputList.append(self.getXmlMovie(element, None))
            elif element.tag == 'series':
                inputList.extend(self.getXmlSeries(element))
            else:
                print('Unknown tag: {}'.format(element.tag))
        return inputList


    def getXmlSeries(self, series):
        """
        Obtain the series information and movies in the series.
        """

        seriesList = []
        seriesTitle = None
        for child in series.iterchildren(tag='title'):
            seriesTitle = child.text
        seriesList.append(Movie(title=seriesTitle))

        # get the movies in the series
        for movie in series.iterchildren(tag='movie'):
            seriesList.append(self.getXmlMovie(movie, seriesTitle))

        return seriesList


    def getXmlMovie(self, movieElement, seriesTitle):
        """
        Extract xml data as a Movie object.
        """

        movie = Movie(series=seriesTitle)
        directorList = []
        starList = []
        genreList = []

        for data in movieElement.iterchildren(tag='title'):
            movie.title = data.text
        for data in movieElement.iterchildren(tag='date'):
            movie.date = data.text
        for data in movieElement.iterchildren(tag='director'):
            directorList.append(data.text)
        movie.director = '; '.join(directorList)
        for data in movieElement.iterchildren(tag='duration'):
            movie.duration = data.text
        for data in movieElement.iterchildren(tag='star'):
            starList.append(data.text)
        movie.stars = '; '.join(starList)
        for data in movieElement.iterchildren(tag='genre'):
            genreList.append(data.text)
        movie.genre = '; '.join(genreList)
        for data in movieElement.iterchildren(tag='media'):
            movie.media = data.text

        return movie


    def populateMovieTreeStore(self, movieList):
        """
        Populate the treeStore from a list of movies.
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
