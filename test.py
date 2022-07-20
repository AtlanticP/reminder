import unittest
import tkinter as tk
from collections import namedtuple
from datetime import datetime, timedelta

from main import App
from task import TaskWindow
from task import Note
#%%
@unittest.skip
class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.root = App()
        self.root.general_properties()
        self.root.set_widgets()
        self.root.current_time()
        self.root.dooneevent()
        
    def tearDown(self):
        self.root.destroy()
    
    # def test_root_children(self):
    #     set(self.root.children().values())
    
    def test_button_task_exists(self):
        but_task = self.root.winfo_children()[-1] ##########
        expected = tk.Button
        self.assertEqual(expected, type(but_task))
        
    def test_button_task_text(self):
        but_task = self.root.winfo_children()[-1]
        expected = "task"
        self.assertEqual(expected, but_task["text"])
        
    def test_create_task_win(self):
        self.root.create_task()
        childs = (type(i) for i in self.root.winfo_children())
        self.assertIn(tk.Toplevel, childs)


# @unittest.skip        
class TestTaskWindow(unittest.TestCase):

    def setUp(self):
        self.root = TaskWindow()
        self.root._window_task()
     
    def tearDown(self):
        self.root.destroy()
        
    def test_window_task_exists(self):
        childs = (type(i) for i in self.root.winfo_children())
        self.assertIn(tk.Toplevel, childs)
        
    def test_textarea_exists(self):
        top_level = next(i for i in self.root.winfo_children() if isinstance(i, tk.Toplevel))
        top_level_children = (type(i) for i in top_level.winfo_children())
        msg = "tk.Toplevel object has no tk.Text for text area"
        self.assertIn(tk.Text, top_level_children, msg)
    
    def test_textarea_placeholder(self):
        pass
        
    def test_save_button(self):
        top_level = next(i for i in self.root.winfo_children() if isinstance(i, tk.Toplevel))
        top_level_children = (type(i) for i in top_level.winfo_children())
        msg = "tk.Toplevel object has no tk.Button"
        # import pdb; pdb.set_trace()
        self.assertIn(tk.Button, top_level_children, msg)
        
    def test_save_note_saves(self):
        self.root._save_note()
        notes = self.root.notes
        msg = "save_note funtion works wrong"
        self.assertNotEqual(len(notes), 0, msg)
        
    def test_save_note_instance(self):
        self.root._save_note()
        self.assertIsInstance(self.root.notes[0], Note)

    @unittest.skip
    def test_save_more(self):
        pass        
    
if __name__ == "__main__":
    unittest.main()
        
        
        
        
        
        
