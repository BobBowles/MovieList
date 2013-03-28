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

class Movie(object):
    """
    A data wrapper for managing movie data.
    """


    def __init__(self,
                 title=None,
                 date=2000,
                 director=None,
                 duration=90,
                 stars=None,
                 genre=None,
                 media=None):
        """
        Initialize a movie's data attributes.
        """

        self.title = title
        self.date = date
        self.director = director
        self.duration = duration
        self.stars = stars
        self.genre = genre
        self.media = media


    def toList(self):
        """
        Publish the movie data as a list.
        """

        return [self.title,
                self.date,
                self.director,
                self.duration,
                self.stars,
                self.genre,
                self.media,
                ]


    def __repr__(self):

        return ("Movie(title='{0.title}', "
                "date={0.date}, "
                "director='{0.director}', "
                "duration={0.duration}, "
                "stars='{0.stars}', "
                "genre='{0.genre}', "
                "media='{0.media}')"
                ).format(self)
