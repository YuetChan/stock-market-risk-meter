class core_manager:
  
    def add_dir_tree(
        self, 
        dir_tree
        ):
        self.dir_trees.append(dir_tree)


    def remove_dir_tree(
        self, 
        id
        ):
        dir_trees  = self.dir_trees

        for tree in dir_trees:
          if tree.id == id:
            dir_trees.remove(tree)

