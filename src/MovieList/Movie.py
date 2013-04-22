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
Module: MovieList.Movie
Created on: 28 Mar 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""


# constants to define sensible default values
DEFAULT_DATE = ''
DEFAULT_DURATION = ''
DEFAULT_TEXT = ''


class Movie(object):
    """
    A data wrapper for managing movie data.
    """


    def __init__(self,
                 title='',
                 date=DEFAULT_DATE,
                 director=DEFAULT_TEXT,
                 duration=DEFAULT_DURATION,
                 stars=DEFAULT_TEXT,
                 genre=DEFAULT_TEXT,
                 media=DEFAULT_TEXT,
                 series=None,
                 ):
        """
        Initialize a movie's data attributes.

        Some care is needed converting nulls between ints and strings for the
        'numeric' fields date and duration.
        """

        self.title = title
        self.date = '{0:>4s}'.format(str(date)) if date else ''
        self.director = director
        self.duration = '{0:>3s}'.format(str(duration)) if duration else ''
        self.stars = stars
        self.genre = genre
        self.media = media
        self.series = series


    def toList(self):
        """
        Publish the movie data as a list.

        The order of parameters in the list is:
        0    title        the name of the movie
        1    date         the year of publication (if known)
        2    director     the director(s) (;-separated list)
        3    duration     the time the movie runs for (mins)
        4    stars        the main stars cited (;-delimited list)
        5    genre        the movie's genre (;-delimited list)
        6    media        the location of the movie file on the local system
        7    series       the name of the series the movie belongs to (or None)
        """

        # fix for legacy versions with numeric attributes
        date = '{0:>4s}'.format(str(self.date)) if self.date else ''
        duration = '{0:>3s}'.format(str(self.duration)) if self.duration else ''

        # fix for legacy versions with no series attribute
        try:
            return [self.title,
                    date,
                    self.director,
                    duration,
                    self.stars,
                    self.genre,
                    self.media,
                    self.series,
                    ]
        except AttributeError as e:
            return [self.title,
                    date,
                    self.director,
                    duration,
                    self.stars,
                    self.genre,
                    self.media,
                    None,
                    ]


    @staticmethod
    def fromList(listObject):
        """
        Convert a list-like object into a Movie.

        This reverses the effect of self.toList(), and assumes the same order of
        parameters in the list.
        """

        return Movie(title=listObject[0],
                     date=listObject[1],
                     director=listObject[2],
                     duration=listObject[3],
                     stars=listObject[4],
                     genre=listObject[5],
                     media=listObject[6],
                     series=listObject[7],
                     )


    def __repr__(self):

        series = None
        if self.series:
            series = "'{}'".format(self.series)
        return ("Movie(title='{0.title}', "
                "date={0.date}, "
                "director='{0.director}', "
                "duration={0.duration}, "
                "stars='{0.stars}', "
                "genre='{0.genre}', "
                "media='{0.media}', "
                "series={1})"
                ).format(self, series)


    def __eq__(self, other):

        return self.__dict__ == other.__dict__





if __name__ == '__main__':

    import doctest
    doctest.testmod()
