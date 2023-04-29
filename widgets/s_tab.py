from PyQt5.QtWidgets import QTabWidget

class s_tab(QTabWidget):

    def __init__(
            self, 
            parent=None
            ):
        super(s_tab, self).__init__(parent)


    def connect_tab_changed(
            self, 
            l_func
            ):
        self.currentChanged.connect(
            lambda idx: l_func(idx)
            )   


    def upsert_widget_by_label(
            self, 
            widget, 
            label
            ):
        tab_idx = self._get_tab_index_by_label(label)

        if tab_idx >= 0:
            self.removeTab(tab_idx)
            self.insertTab(tab_idx, widget, label)

        else:
            self.addTab(widget, label)
            tab_idx = self._get_tab_index_by_label(label)


        self.setCurrentIndex(tab_idx)


    # def _on_tab_changed(
    #         self, 
    #         l_func
    #         ):
    #     self.currentChanged.connect(
    #         lambda idx: l_func(idx)
    #         )

    #     # Get the tab widget that emitted the signal
    #     sender = self.sender()
    #     # Get the current tab index
    #     current_tab_index = sender.currentIndex()

    #     # Get the text of the current tab
    #     current_tab_text = sender.tabText(current_tab_index)
    #     print("Clicked Tab Index:", current_tab_index)
    #     print("Clicked Tab Text:", current_tab_text)


    def _get_tab_index_by_label(
            self, 
            label
            ):
        idx = -1

        for i in range(self.count()):
            if self.tabBar().tabText(i) == label:
                idx = i

                break

    
        return idx
    
