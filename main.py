import gi
import os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

class EditorWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Editor")

        box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        textView = Gtk.TextView()
        toolBar = self.createToolBar(textView)
        box.pack_start(toolBar, False, False, 0)
        box.pack_start(textView, True, True, 0)

        self.add(box)

    def createToolBar(self, textView):
        toolBar = Gtk.Toolbar()

        textBuffer = textView.get_buffer()
        
        openButton = Gtk.ToolButton()
        openButton.set_icon_name("open-document")
        openButton.connect("clicked", self.openBuffer, textBuffer)
        toolBar.insert(openButton, -1)
        
        toolBar.insert(Gtk.SeparatorToolItem(), -1)
        
        saveButton = Gtk.ToolButton()
        saveButton.set_icon_name("document-save-as")
        saveButton.connect("clicked", self.saveBuffer, textBuffer)
        toolBar.insert(saveButton, -1)

        toolBar.insert(Gtk.SeparatorToolItem(), -1)

        boldButton = Gtk.ToolButton()
        boldButton.set_icon_name("format-text-bold")
        boldTag = textBuffer.create_tag("bold", weight = Pango.Weight.BOLD)
        boldButton.connect("clicked", lambda widget:
            textBuffer.apply_tag(boldTag, *textBuffer.get_selection_bounds())
        )
        toolBar.insert(boldButton, -1)

        italicButton = Gtk.ToolButton()
        italicButton.set_icon_name("format-text-italic")
        italicTag = textBuffer.create_tag("italic", style = Pango.Style.ITALIC)
        italicButton.connect("clicked", lambda widget:
            textBuffer.apply_tag(italicTag, *textBuffer.get_selection_bounds())
        )
        toolBar.insert(italicButton, -1)

        underlineButton = Gtk.ToolButton()
        underlineButton.set_icon_name("format-text-underline")
        underlineTag = textBuffer.create_tag("underline", underline = Pango.Underline.SINGLE)
        underlineButton.connect("clicked", lambda widget:
            textBuffer.apply_tag(underlineTag, *textBuffer.get_selection_bounds())
        )
        toolBar.insert(underlineButton, -1)

        strikethroughButton = Gtk.ToolButton()
        strikethroughButton.set_icon_name("format-text-strikethrough")
        strikethroughTag = textBuffer.create_tag("strikethrough", strikethrough = True)
        strikethroughButton.connect("clicked", lambda widget:
            textBuffer.apply_tag(strikethroughTag, *textBuffer.get_selection_bounds())
        )
        toolBar.insert(strikethroughButton, -1)

        toolBar.insert(Gtk.SeparatorToolItem(), -1)
        
        toolButton = Gtk.ToolButton()
        toolButton.set_icon_name("preferences-desktop-font")
        toolButton.connect("clicked", self.setFont, textBuffer)
        toolBar.insert(toolButton, -1)

        return toolBar

    def saveBuffer(self, widget, textBuffer):
        saveDialog = Gtk.FileChooserDialog()
        saveDialog.set_action(Gtk.FileChooserAction.SAVE)
        saveDialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        saveDialog.add_button("Save As", Gtk.ResponseType.OK)

        response = saveDialog.run()
        if response != Gtk.ResponseType.OK:
            saveDialog.destroy()
            return

        path = os.path.join(saveDialog.get_current_folder(), saveDialog.get_filename())
        bounds = textBuffer.get_bounds()
        serializationFormat = textBuffer.register_serialize_tagset()
        serial = textBuffer.serialize(textBuffer, serializationFormat, *bounds)
        with open(path, 'wb') as outputFile:
            outputFile.write(serial)

        saveDialog.destroy()

    def setFont(self, widget, textBuffer):
        fontChooserDialog = Gtk.FontChooserDialog()
        fontChooserDialog.set_title("FontChooserDialog")
        response = fontChooserDialog.run()

        if response != Gtk.ResponseType.OK:
            fontChooserDialog.destroy()
            return

        fontDescriptor = fontChooserDialog.get_font_desc()
        tagTable = textBuffer.get_tag_table()
        tagName = fontDescriptor.to_string()
        tag = tagTable.lookup(tagName)
        if tag is None:
            tag = textBuffer.create_tag(tagName, font_desc=fontDescriptor)
        textBuffer.apply_tag(tag, *textBuffer.get_selection_bounds())
        fontChooserDialog.destroy()
        
    def openBuffer(self, widget, textBuffer):
        openDialog = Gtk.FileChooserDialog()
        openDialog.set_action(Gtk.FileChooserAction.OPEN)
        openDialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        openDialog.add_button("OPEN", Gtk.ResponseType.OK)
        
        response = openDialog.run()
        if response != Gtk.ResponseType.OK:
            openDialog.destroy()
            return
        path = os.path.join(openDialog.get_current_folder(), openDialog.get_filename())
        bounds = textBuffer.get_bounds()
        deserializationFormat = textBuffer.register_deserialize_tagset()
        deserial = textBuffer.deserialize(textBuffer, deserializationFormat, text, data)
        with open(path, 'rb') as outputFile:
            data = outputFile.read()
            textBuffer.set_text(text)
        openDialog.destroy()
        
editorWindow = EditorWindow()
editorWindow.connect("destroy", Gtk.main_quit)
editorWindow.show_all()
Gtk.main()
