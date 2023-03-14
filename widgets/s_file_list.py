from PyQt5.QtWidgets import QListView

class s_file_list(QListView):

  def __init__(
        self, 
        src_model,
        parent=None
        ):
      super(s_file_list, self).__init__(parent)

      self.src_model = src_model
    
    
  def handleDoubleClick(
        self, 
        item
        ):
      print("Double clicked on item:", item.text())