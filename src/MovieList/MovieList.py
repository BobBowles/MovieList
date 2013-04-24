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

import os, subprocess
from gi.repository import Gtk, Gdk
from constants import UI_BUILD_FILE, UI_CSS_FILE
from Movie import Movie, MovieSeries
from MovieEditDialog import MovieEditDialog
from MovieListIO import MovieListIO

# test only
from testData import testMovies

# 'constants' for statusbar io
ADD = 'add'
EDIT = 'edit'
DELETE = 'delete'
PLAY = 'play'
OK = 0
ABORT = 1
WARN = 2
CONTEXT = {ADD: ['Added: {} ({})', 'Add aborted', ''],
           EDIT: ['Edited: {} ({})', 'Edit aborted',
                  'Edit: Select a movie to edit'],
           DELETE: ['Deleted: {} ({})', 'Delete aborted',
                    'Delete: Select a movie to delete'],
           PLAY: ['Played: {}', 'Play aborted',
                  'Play: no media to play']
           }


class MovieList:
    """
    The MovieList object
    """


    def __init__(self):
        """
        Initialize the MovieList's components.

        Load the UI elements from the .glade file. Add an IO module to handle
        data files.
        """

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_BUILD_FILE)
        self.builder.connect_signals(self)

        # TODO: references to the widgets we need to manipulate
        # self.movieListStore = self.builder.get_object('movieListStore')
        self.movieTreeStore = self.builder.get_object('movieTreeStore')

        self.movieTreeView = self.builder.get_object('movieTreeView')
        self.movieTreeSelection = self.builder.get_object('movieTreeSelection')
        self.statusbar = self.builder.get_object('statusbar')
        self.fileSaveAction = self.builder.get_object('fileSaveAction')

        # apply any non-standard column rendering
        self.customiseRendering()

        # add the io module
        self.movieListIO = MovieListIO(self)

        # use the io module to populate with the test data
        self.movieListIO.populateMovieTreeStore(testMovies)

        # initialize internal flags for the data status
        self.__filename = None
        self.__dirty = True
        self.setDirty(False)

        # get a reference to the main window itself and display the window
        self.window = self.builder.get_object('window')
        self.window.show_all()


    # TODO: other action(s) go here

    def customiseRendering(self):
        """
        Apply custom rendering to the columns of the movieTreeView.

        This is a workaround for not (apparently?) being able to do this in
        Glade. We don't need to refer to the renderers elsewhere, so local
        variables are enough for our purposes.
        """

        # deal with justification of numeric columns.
        self.setXAlignment('durationRenderer')
        self.setXAlignment('dateRenderer')

        # set word wrapping on long text items (title, stars, other??)
        self.setColumnWordWrap('titleRenderer', 'titleColumn')
        self.setColumnWordWrap('directorRenderer', 'directorColumn')
        self.setColumnWordWrap('starsRenderer', 'starsColumn')
        self.setColumnWordWrap('genreRenderer', 'genreColumn')


    def setXAlignment(self, rendererName):
        """
        Set the renderer to display text right-aligned.
        """

        renderer = self.builder.get_object(rendererName)
        renderer.props.xalign = 1.0


    def setColumnWordWrap(self, rendererName, columnName):
        """
        Set word wrap on the given column.

        The word wrap policy is set in the renderer, using the minimum width of
        the column.
        """

        renderer = self.builder.get_object(rendererName)
        renderer.props.wrap_mode = Gtk.WrapMode.WORD
        renderer.props.wrap_width = \
            self.builder.get_object(columnName).get_min_width()


    def setDirty(self, dirty):
        """
        Set the dirty data flag.

        Ensure the save action can only be activated when the data is dirty.
        """

        if dirty != self.__dirty:
            self.__dirty = dirty
            self.fileSaveAction.set_sensitive(dirty)


    def chooseSaveFile(self, title, fileSelectionMode):
        """
        File selection dialog.

        The parameters determine whether the dialog is used for opening or
        saving the file. The chosen file is saved internally for future
        reference.
        Returns whether a satisfactory choice was made.
        """

        # select the stock button to use according to the selection mode
        okButtonType = None
        if fileSelectionMode == Gtk.FileChooserAction.OPEN:
            okButtonType = Gtk.STOCK_OPEN
        else:
            okButtonType = Gtk.STOCK_SAVE

        fileChooserDialog = Gtk.FileChooserDialog(title + '...',
                                                  self.window,
                                                  fileSelectionMode,
                                                  [Gtk.STOCK_CANCEL,
                                                   Gtk.ResponseType.CANCEL,
                                                   okButtonType,
                                                   Gtk.ResponseType.OK])
        response = fileChooserDialog.run()
        ok = response == Gtk.ResponseType.OK
        if ok:
            self.__filename = fileChooserDialog.get_filename()
            print('Chosen file {}'.format(self.__filename))
        fileChooserDialog.destroy()
        return ok


    def getFileName(self):
        return self.__filename


    def save(self, context):
        self.movieListIO.save()
        self.statusbar.push(context, 'Saved As: {}'.format(self.__filename))
        self.setDirty(False)


    # TODO: File menu and toolbar actions

    def on_fileNewAction_activate(self, widget):
        """
        Handler for the file new action.

        Clear out any existing data, start the tree from an empty data store.
        """

        context = self.statusbar.get_context_id('new')
        self.movieTreeStore.clear()
        self.setDirty(False)
        self.__filename = None
        self.statusbar.push(context, 'New: empty movie list created')


    def on_fileOpenAction_activate(self, widget):
        """
        Handler for the file open action.

        Clear existing data and load new data from a file.
        """

        context = self.statusbar.get_context_id('open')

        # choose a file
        if self.chooseSaveFile('Open', Gtk.FileChooserAction.OPEN):
            self.movieListIO.load()
            self.statusbar.push(context,
                                'Opened: {}'.format(self.__filename)
                                )
            self.setDirty(False)
        else:
            self.statusbar.push(context, 'Open: open aborted')


    def on_fileSaveAction_activate(self, widget):
        """
        Handler for the file save action.

        Save the current data in the file it came from. If no file can be
        identified, resort to the 'save as' action.
        """

        context = self.statusbar.get_context_id('save')
        if not self.__filename:
            self.on_fileSaveAsAction_activate(widget)
        else:
            self.save(context)


    def on_fileSaveAsAction_activate(self, widget):
        """
        Handler for the file save as action.

        Choose a file to save to, and save the data.
        """

        context = self.statusbar.get_context_id('save')

        # choose a file
        if self.chooseSaveFile('Save', Gtk.FileChooserAction.SAVE):
            self.save(context)
        else:
            self.statusbar.push(context, 'Save As: save aborted')


    def on_fileQuitAction_activate(self, widget):
        """
        Handler for the file quit action.

        This implementation just passes on responsibility to on_window_destroy().
        """

        self.on_window_destroy(widget)


    # Edit menu, toolbar and context actions

    def on_playAction_activate(self, widget):
        """
        Handler for the play action.

        Play the movie using an external application.
        """

        contextId = self.statusbar.get_context_id(PLAY)
        treeIndex, movie = self.getMovieFromSelection(contextId, PLAY)

        # ensure media file is not blank
        filename = movie.media
        if not filename or not os.path.exists(filename):
            self.displaySelectMovieErrorMessage(contextId, PLAY)
            return

        # play the media
        # TODO: VLC  Media Player on *nix is assumed here
        system = subprocess.call('vlc "{}"'.format(filename), shell=True)
        self.statusbar.push(contextId, CONTEXT[PLAY][OK].format(filename))


    def on_addAction_activate(self, widget):
        """
        Handler for the movie add action. Add a new movie to the list.

        Displays a new empty movie in the edit dialog. If the movie information
        is changed, add the movie information to the list.
        """

        # the statusbar context
        contextId = self.statusbar.get_context_id(ADD)

        # an empty movie object to fill in
        movie = Movie()
        seriesIndex = seriesName = None
        response, newMovie, newSeriesName = self.editMovieDialog(movie,
                                                                 seriesName)
        newSeriesIndex = self.getSeriesIndexFromName(newSeriesName)

        # update the model and display
        self.updateMovieEntry(contextId, ADD, None, response,
                              movie, seriesIndex,
                              newMovie, newSeriesIndex)


    def on_editAction_activate(self, widget):
        """
        Handler for the movie edit action. Edit the selected movie.

        Takes the current selected movie and displays it in the edit dialog. If
        the movie information is changed, update the movie information in the
        list.
        """

        # context of statusbar messages
        contextId = self.statusbar.get_context_id(EDIT)

        # do the edit
        treeIndex, movie = self.getMovieFromSelection(contextId, EDIT)
        seriesIndex, seriesName = self.findMovieSeries(treeIndex)
        response, editedMovie, editedSeriesName = \
            self.editMovieDialog(movie, seriesName)

        editedSeriesIndex = (self.getSeriesIndexFromName(editedSeriesName)
                             if editedSeriesName != seriesName
                             else seriesIndex)

        # update the model and display
        self.updateMovieEntry(contextId, EDIT, treeIndex, response,
                              movie, seriesIndex,
                              editedMovie, editedSeriesIndex)


    def findMovieSeries(self, movieIndex):
        """
        Get the details of the series a movie belongs to using its tree index.
        """

        seriesIndex = self.movieTreeStore.iter_parent(movieIndex)
        seriesTitle = (self.movieTreeStore[seriesIndex][0]
                       if seriesIndex else None)
        return seriesIndex, seriesTitle


    def getSeriesIndexFromName(self, seriesTitle):
        """
        Obtain the treeStore pointer for the series from the name of the series.
        """

        treeIter = self.movieTreeStore.get_iter_first()
        while treeIter:
            if seriesTitle == self.movieTreeStore[treeIter][0]:
                return treeIter
            treeIter = self.movieTreeStore.iter_next(treeIter)
        treeIter = None


    def on_deleteAction_activate(self, widget):
        """
        Handler for the movie delete action. Delete the selected movie.

        Confirmation is required.
        """

        # context of statusbar messages
        contextId = self.statusbar.get_context_id(DELETE)

        # get the current movie selection
        treeIndex, movie = self.getMovieFromSelection(contextId, DELETE)

        # invoke the confirmation dialog
        dialog = Gtk.MessageDialog(self.window,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   'Confirm delete of movie {} ({})'
                                   .format(movie.title, movie.date),
                                   )
        dialog.set_decorated(False)
        response = dialog.run()
        dialog.destroy()

        # update the display
        self.updateMovieEntry(contextId, DELETE, treeIndex, response,
                              movie, None, None, None)


    def getMovieFromSelection(self, contextId, context):
        """
        Obtain a movie from the currently-selected treeView row.
        """

        # get the current movie selection
        treeModel, treeIndex = self.movieTreeSelection.get_selected()
        if treeModel is None or treeIndex is None:
            self.displaySelectMovieErrorMessage(contextId, context)
            return
        return treeIndex, Movie.fromList(treeModel[treeIndex])


    def displaySelectMovieErrorMessage(self, contextId, context):
        """
        Error message for functions that need a treeview selection.

        This started as a helper for edit/delete functions, but now it is also
        used by the play tool.
        """

        dialog = Gtk.MessageDialog(self.window, Gtk.DialogFlags.MODAL,
            Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK,
            CONTEXT[context][WARN].format(context))
        dialog.set_decorated(False)
        dialog.run()
        dialog.destroy()
        self.statusbar.push(contextId, CONTEXT[context][WARN].format(context))
        return


    def editMovieDialog(self, movie, seriesName):
        """
        Invoke the dialog.
        """

        dialog = MovieEditDialog(parent=self.window,
                                 movie=movie, seriesName=seriesName,
                                 movieTreeStore=self.movieTreeStore)
        return dialog.run()


    def updateMovieEntry(self, contextId, context, treeIndex, response,
                         originalMovie, originalSeriesIndex,
                         modifiedMovie, modifiedSeriesIndex):
        """
        Update the model and display.
        """

        if (response == Gtk.ResponseType.OK and
            ((modifiedMovie != originalMovie
              if modifiedMovie else True) or
             (modifiedSeriesIndex != originalSeriesIndex
              if modifiedSeriesIndex else True))):

            # to delete or edit we remove the old entry
            if context == DELETE or context == EDIT:
                # if the 'movie' entry has children re-parent them to the root
                if self.movieTreeStore.iter_has_child(treeIndex):
                    self.reParentChildren(treeIndex, modifiedSeriesIndex)
                # ... then delete the parent
                self.movieTreeStore.remove(treeIndex)

            # to edit or add we add the modified/added entry
            if context == ADD or context == EDIT:
                self.movieListIO.appendMovieToStore(modifiedMovie,
                                                    modifiedSeriesIndex)
            title, date = ((modifiedMovie.title, modifiedMovie.date)
                           if modifiedMovie else
                           (originalMovie.title, originalMovie.date))
            self.statusbar.push(contextId,
                                CONTEXT[context][OK].format(title, date))

            self.setDirty(True)

        else:
            self.statusbar.push(contextId, CONTEXT[context][ABORT])


    def reParentChildren(self, seriesIter, newSeriesIter):
        """
        Take the children of a series to be deleted and re-parent them to the
        root, or another named series.
        """

        childIter = self.movieTreeStore.iter_children(seriesIter)
        # moviesToAdd = []
        while childIter:
            movie = Movie.fromList(self.movieTreeStore[childIter])
            self.movieTreeStore.remove(childIter)
            self.movieListIO.appendMovieToStore(movie, newSeriesIter)
            childIter = self.movieTreeStore.iter_children(seriesIter)


    # TODO: Tools menu actions

    def on_importAction_activate(self, widget):
        """
        Handler for the import action.

        Load csv data from a file.
        """

        context = self.statusbar.get_context_id('import')

        # choose a file
        if self.chooseSaveFile('Import', Gtk.FileChooserAction.OPEN):
            self.movieListIO.importCsv()
            self.statusbar.push(context,
                                'Imported: {}'.format(self.__filename)
                                )
            self.setDirty(True)
            self.__filename = None
        else:
            self.statusbar.push(context, 'Import: import aborted')


    # TODO: Help menu actions


    # Context menu actions

    def on_movieTreeView_button_press_event(self, widget, event):
        """
        Handler for mouse clicks on the tree view.

        Single L-click: change current selection (this is automatic).
        Double L-click: launch movie.
        R-click: Display the edit menu as a context popup.

        (Note: the edit menu is connected in Glade to the movieTreeView
        button_press_event as data, and swapped. So, the menu is passed to this
        handler as the widget, instead of the treeView.)
        """

        # double-click launches movie application
        if (event.button == Gdk.BUTTON_PRIMARY and
            event.type == Gdk.EventType._2BUTTON_PRESS):
            self.on_playAction_activate(widget)

        # right-click activates the context menu
        if event.button == Gdk.BUTTON_SECONDARY:
            widget.popup(None, None, None, None,
                         Gdk.BUTTON_SECONDARY, event.get_time())


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
