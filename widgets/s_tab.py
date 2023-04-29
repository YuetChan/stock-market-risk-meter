from PyQt5.QtWidgets import QTabWidget

class s_tab(QTabWidget):
    
    def __init__(
        self, 
        parent=None
        ):
        super(s_tab, self).__init__(parent)


    def _get_tab_index_by_label(self, label):
        idx = -1

        for i in range(self.count()):
            if self.tabBar().tabText(i) == label:
                idx = i
                
                break

    
        return idx
    

    def upsert_widget_by_label(self, widget, label):
        tab_idx = self._get_tab_index_by_label(label)

        if tab_idx >= 0:
            self.removeTab(tab_idx)
            self.insertTab(tab_idx, widget, label)

        else:
            self.addTab(widget, label)
            tab_idx = self._get_tab_index_by_label(label)


        self.setCurrentIndex(tab_idx)

