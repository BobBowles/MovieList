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
Module: MovieList.TreeModelHelper
Created on: 8 Jun 2013
@author: Bob Bowles <bobjohnbowles@gmail.com>
"""

from gi.repository import Gtk



class TreeModelHelper(object):
    """
    A wrapper for a Gtk.TreeModel to provide supplementary methods.

    The main aim is to provide a way to drill into the model layers to get to
    the TreeStore data the model is based on.
    """


    def __init__(self, model=None,
                 comboBox=None, treeStore=None, filterMethod=None):
        """
        Initialise the model the helper is for.

        If the model is provided comboBox, treeStore, and filterMethod are
        ignored.
        If the model is NOT provided, comboBox and treeStore must be provided.
        If a filter is required, the filterMethod to use on the data must be
        provided.
        """

        if model:
            self.model = model
        else:
            self.createModelForComboBox(comboBox, treeStore, filterMethod)


    def createModelForComboBox(self, comboBox=None, treeStore=None,
                               filterMethod=None):
        """
        Create a model of the Gtk.TreeStore data suitable for a Gtk.ComboBox.

        Use the supplied filter method to create a filter model, then add a sort
        model with standard sorting.
        """

        # TODO: this is lowest common denominator. Need filter and sort
        self.model = treeStore
        comboBox.set_model(self.model)


    def getUnderlyingSelection(self, iter):
        """
        Drill down into the child models of the view to find the base model and
        iteration of the current selection.
        """

        parentModel, parentIter = self.model, iter
        while True:
            childModel = parentModel.get_model()
            childIter = parentModel.convert_iter_to_child_iter(parentIter)
            if isinstance(childModel, Gtk.TreeStore):
                return childModel, childIter
            else:
                parentModel = childModel
                parentIter = childIter
