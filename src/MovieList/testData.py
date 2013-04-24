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
Module: MovieList.testData
Created on: 24 Apr 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

from Movie import Movie, MovieSeries

# test data
testMovies = [
              Movie(title='A Test',
                    date=1999,
                    director='Bob Bowles',
                    duration=30,
                    stars='Bob Bowles; Zhang Dehua',
                    genre='Western',
                    ),
              MovieSeries(title='This Is The Test Series',
                          series=[
                                  Movie(title='This Is Test Movie 1',
                                        date=2000,
                                        director='Bob Bowles',
                                        duration=60,
                                        stars='Zhang Dehua; Bob Bowles; Mum',
                                        genre='Fantasy Football',
                                        media='avi',
                                        ),
                                  Movie(title='This Is Test Movie 2',
                                        date=2001,
                                        director='Bob Bowles',
                                        duration=90,
                                        stars='Bob Bowles; Mum; Zhang Dehua',
                                        genre='Domestic Drama',
                                        media='dvd',
                                        ),
                                  Movie(title='This Is Test Movie 3',
                                        date=2005,
                                        director='Bob Bowles',
                                        duration=120,
                                        stars='Mum; Zhang Dehua; Bob Bowles',
                                        genre='Documentary',
                                        media='stream',
                                        ),
                                  ],
                          ),
              Movie(title='Yet Another One Not In The Series',
                    date=2006,
                    director='Mum',
                    duration=10,
                    stars='Mum, Bob Bowles',
                    genre='Soap Opera',
                    ),
              ]


if __name__ == '__main__':
    print('Test movies:\n' + '\n'.join('{}'.format(movie)
                                       for movie in testMovies))
