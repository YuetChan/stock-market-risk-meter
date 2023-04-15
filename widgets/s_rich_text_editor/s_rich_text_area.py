from bs4 import BeautifulSoup
import hashlib

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeyEvent, QTextListFormat, QTextCursor, QKeySequence, QFont
from PyQt5.QtWidgets import QTextEdit, QApplication

from widgets.s_find_dialog import s_find_dialog
from widgets.s_text_area import s_text_area

# This class is designed to track key press events 
# and dynamically update the tool bar based on those events.

# Additionally, it manages clipboard behavior 
# and provides methods for text highlighting and search functionality
class s_rich_text_area(s_text_area):

    text_changed = pyqtSignal(dict)

    def __init__(
            self, 
            parent=None
            ):
        super(s_rich_text_area, self).__init__(parent)

        self.qt_clipbrd_cache = { }

        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
        self.textChanged.connect(self._on_text_changed)
        

    def set_tool_bar(
            self, 
            rich_text_tool_bar
            ):
        self.rich_text_tool_bar = rich_text_tool_bar


    def keyPressEvent(
            self, 
            event: QKeyEvent
            ):
        clipbrd = QApplication.clipboard()

        cursor = self.textCursor()

        rich_text_tool_bar = self.rich_text_tool_bar

        if self._is_delete_key(event):
            if self._is_delete_on_empty_line(cursor) and self._is_list_above(cursor):
                super().keyPressEvent(event)

                self._create_empty_list(cursor)
                rich_text_tool_bar.toggle_bullet_point(True) 

            elif self._is_delete_on_empty_list(cursor):
                super().keyPressEvent(event)

                was_in_bullet_pt = not self._is_list(cursor) and rich_text_tool_bar.is_bullet_point_checked()

                if was_in_bullet_pt:
                    self._reset_indent(cursor)
                    rich_text_tool_bar.toggle_bullet_point(False) 


            else:
                super().keyPressEvent(event)


        elif self._is_copy_key(event) or self._is_cut_key(event):
            # Copy / cut the htnl to clipbrd first
            # By default, qt makes small adjustment to clipbrd html 
            super().keyPressEvent(event)

            cursor = self.textCursor()
            
            clipbrd_html = clipbrd.mimeData().html()
            stripped_html = clipbrd_html

            if self._is_list(cursor) and self._is_start_of_line(cursor) and not self._is_on_first_line(cursor):
                stripped_html = self._strip_first_p_tag(stripped_html)

            
            stripped_html = self._strip_qt_start_and_end_segments_tags(stripped_html)

            new_cache = { }
            new_cache[self._get_hash_of_str(clipbrd_html)] = stripped_html 

            self._set_qt_clipboard_cache(new_cache)

        elif self._is_paste_key(event):
            clipbrd_html = clipbrd.mimeData().html()
            hashed_html = self._get_hash_of_str(clipbrd_html)

            html = ''

            if self._is_the_same_qt_clipboard_cache(hashed_html):
                cursor = self.textCursor()
                html = self.qt_clipbrd_cache[hashed_html]
                
            else:
                html = self._sanitize_tags(clipbrd_html)

            
            cursor.insertHtml(html)


# Enforce default block format, font family, font size on pasted text
# --------------------------------------------------------------------
            cursor_pos = cursor.position()

            # Ctrl + a
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            
            charFormat = cursor.charFormat()

            font = charFormat.font()
            font.setFamily('ubuntu')

            charFormat.setFont(font)

            cursor.setCharFormat(charFormat)

            self.setTextCursor(cursor)

            cursor.setPosition(cursor_pos)

            self.setTextCursor(cursor)


# --------------------------------------------------------------------

        else:
            super().keyPressEvent(event)


    def _on_cursor_position_changed(self):
        cursor = self.textCursor()

        block_fmt = cursor.blockFormat()


# When text is pasted at the start of text edit area,
# the pos -1 will have non default char and block format

# So this is the hack to enforce default block format, font family, font size
# --------------------------------------------------------------------
        if block_fmt.topMargin() > 0 or block_fmt.bottomMargin() > 0:
            block_fmt.setTopMargin(0)
            block_fmt.setBottomMargin(0)

            cursor.setBlockFormat(block_fmt)

            self.setTextCursor(cursor)


        char_fmt = cursor.charFormat()

        font = char_fmt.font()

        if font.family != 'ubuntu':
            font.setFamily('ubuntu')
            font.setPointSize(11)

            char_fmt.setFont(font)

            cursor.setCharFormat(char_fmt)

            self.setTextCursor(cursor)


# --------------------------------------------------------------------

        alignment_int = int(block_fmt.alignment())

        action_map = self.rich_text_tool_bar.action_map

        action_map['bold_action'].setChecked(True if font.bold() else False)
        action_map['italic_action'].setChecked(True if font.italic() else False)
        action_map['underline_action'].setChecked(True if font.underline() else False)

        action_map['bullet_action'].setChecked(True if cursor.currentList() else False)

        action_map['left_align_action'].setChecked(True if alignment_int & Qt.AlignLeft else False)
        action_map['center_align_action'].setChecked(True if alignment_int & Qt.AlignCenter else False)
        action_map['right_align_action'].setChecked(True if alignment_int & Qt.AlignRight else False)


    def _on_text_changed(self):
        self.text_changed.emit({})


    def _is_copy_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Copy)        


    def _is_cut_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Cut) 


    def _is_paste_key(
            self, 
            event
            ):
        return event.matches(QKeySequence.Paste)  


    def _is_delete_key(
            self, 
            event
            ):
        return event.key() == Qt.Key_Backspace


    def _is_delete_on_empty_line(
            self, 
            cursor
            ):
        return self._is_start_of_line(cursor) and not self._is_list(cursor)


    def _is_delete_on_empty_list(
            self, 
            cursor
            ):
        return self._is_start_of_line(cursor) and self._is_list(cursor)


    def _is_on_first_line(
            self, 
            cursor
            ):    
        return cursor.blockNumber() == 0


    def _is_start_of_line(
            self, 
            cursor
            ):
        return cursor.positionInBlock() == 0


    def _is_list(
            self, 
            cursor
            ):
        return cursor.currentList() != None


    def _is_list_above(
            self, 
            cursor
            ):
        cursor.movePosition(QTextCursor.Up)
        is_list_above = cursor.currentList() != None
        
        cursor.movePosition(QTextCursor.Down)

        return is_list_above
    

    def _create_empty_list(
            self, 
            cursor
            ):
        list_fmt = QTextListFormat()

        list_fmt.setStyle(QTextListFormat.ListDisc)
        cursor.createList(list_fmt)


    def _reset_indent(
            self, 
            cursor
            ):
        block_fmt = cursor.blockFormat()
        block_fmt.setIndent(0)

        cursor.setBlockFormat(block_fmt)
           
        self.setTextCursor(cursor)


    def _sanitize_tags(
            self, 
            html
            ):
        soup = BeautifulSoup(html, 'html.parser')

        allowed_tags = [
            '!DOCTYPE', 'body', 'html', 'style', 
            'p', 'ul', 'li', 
            'br', 'span', 'b', 
            'i', 'u', 'div', 
            'pre', 'code'
            ]

        for tag in soup.findAll(True):
            if tag.name not in allowed_tags:
                tag.extract()


        return str(soup)


    def _clear_classes(
            self,
            soup
            ):
        for tag in soup.find_all():
            tag.attrs = {}


        return soup


    def _set_qt_clipboard_cache(
            self, 
            cache
            ):
        self.qt_clipbrd_cache = cache


    def _is_the_same_qt_clipboard_cache(
            self, 
            key
            ):
        return  self.qt_clipbrd_cache.get(key) != None


    # Remove <!--StartFragment--> and <!--EndFragment--> 
    # becuase they are sometimes inserted inproperly by QT
    def _strip_qt_start_and_end_segments_tags(
            self, 
            html
            ):
        html = html.replace('<!--StartFragment-->', '')
        html = html.replace('<!--EndFragment-->', '')

        return html
    

    def _strip_first_p_tag(
            self, 
            html
            ):
        soup = BeautifulSoup(html, 'html.parser')

        first_p = soup.find('p')

        if first_p == None:
            return html
        

        first_p.extract()
        
        return str(soup)


    def _get_hash_of_str(
            self,
            _str
            ):
        hash_object = hashlib.sha256()

        hash_object.update(_str.encode())
        hex_digest = hash_object.hexdigest()

        return str(int(hex_digest, 16))
    
