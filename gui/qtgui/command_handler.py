import applogic.tools
import applogic.tools_algos
import arch

from applogic.cmd.command import *
from datastore import CommentPosition
from inspect import InspectWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from dialogs import *


# Build a list of Key_ constants that QT knows
keyList = dict([(getattr(QtCore.Qt, key), key)
    for key in dir(QtCore.Qt) if key.startswith('Key')])


class CommandHandler(object):

    def handleSetStdComment(self, ident, pos=CommentPosition.POSITION_RIGHT):
        oldcomment = self.ds.comments.getCommentText(ident, pos)

        cw = AddCommentWindow(pos, oldcomment)
        rescode = cw.exec_()
        if rescode:
            self.ds.cmdlist.push(
                    CommentCommand(ident, pos, cw.edit.toPlainText()))

    def handleInspect(self, ident):
        rc, info = self.ds.infostore.lookup(ident)
        if rc != self.ds.infostore.LKUP_OK:
            return

        iw = InspectWindow(info)
        iw.show()
        self.iws += [iw]

    def handleSetLabel(self, ident):
        if ident == None:
            return

        oldlabel = self.ds.symbols.getSymbol(ident)

        # FIXME: replace ident with SECTION:addr
        text, ok = QtWidgets.QInputDialog.getText(None,
            "Set Label", "Enter a label for addr %04x" % ident, text=oldlabel)

        if ok and text != oldlabel:
            self.ds.cmdlist.push(SymbolNameCommand(ident, text))

    def handleXrefs(self, addr):
        ds = self.ds

        xrefs_to = ds.xreflist.getXrefsTo(addr)
        if not xrefs_to:
            return

        d = XrefSelectionWindow(ds, xrefs_to)
        rc = d.exec_()

        if rc:
            self.view.navigateToIdent(d.getSelectedAddr())

    def handleCodeFollow(self, addr):
        # Compound command created within codeFollow primitive
        a = self.gui.global_archname
        applogic.tools_algos.codeFollow(self.ds, a, addr)

    def handleFollowJump(self, addr):
        newaddr = applogic.tools.follow(self.ds, addr)
        if not newaddr:
            return

        rc, obj = self.ds.infostore.lookup(addr)

        if rc != self.ds.infostore.LKUP_OK:
            return

        self.view.navigateToIdent(newaddr)

    # Create ascii string command
    def handleAscii(self, addr):
        s = SetTypeCommand(addr, 'ascii')
        self.ds.cmdlist.push(s)

    # Go back in the memory stack
    def handleCodeReturn(self, addr):
        try:
            top, sel = self.view.memstack.pop()
        except IndexError:
            return

        self.view.setTopSelectedIdent(sel, top)

    def handleUndefine(self, ident):
        self.ds.cmdlist.push(SetTypeCommand(ident, None))

    def buildCmdHandlers(self, pairs):
        """ call with a set of pairs such as:
            [ ( "Semicolon", "AddBinary" ) ] """

        self.cmd_handlers = dict([
            (getattr(QtCore.Qt, "Key_%s" % a), getattr(self, "handle%s" % b))
                for a, b in pairs
            ])

    def __init__(self, gui, ds, view):
        self.gui = gui
        self.iws = []
        self.ds = ds
        self.view = view

        handlers = [
            ("I", "Inspect"),
            ("C", "CodeFollow"),
            ('U', "Undefine"),
            ('A', "Ascii"),
            ('X', "Xrefs"),
            ("Return", "FollowJump"),
            ("N", "SetLabel"),
            ("Backspace", "CodeReturn"),
            ("Escape", "CodeReturn"),
            ("Semicolon", "SetStdComment")
            ]

        self.buildCmdHandlers(handlers)

    def handleCommand(self, addr, cmd):
        try:
            self.cmd_handlers[cmd](addr)
        except KeyError:
            print keyList[cmd]
