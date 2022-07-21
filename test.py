import unittest
import tkinter as tk
from datetime import datetime, timedelta
from itertools import takewhile
import os

from main import App
from task import TaskWindow
import csv
#%%


@unittest.skip        
class TestTaskWindow(unittest.TestCase):

    def setUp(self):
        self.root = TaskWindow()
        self.root._window_task()
     
    def tearDown(self):
        self.root.destroy()
    
    @staticmethod    
    def remove_tail_csv(start):
        '''Remove last row when during testing function saves information to tasks.csv'''
        
        fname = "tasks.csv"
        fname_temp = "temp.csv"       

        with open(fname, "r") as infile, open(fname_temp, "w") as outfile:
            reader = csv.reader(infile)
            header = next(reader)
            writer = csv.writer(outfile, header)
            
            writer.writerow(header)
            writer.writerows(
                takewhile(lambda x: x[0] != start, reader))

            os.rename(fname_temp, fname)
        
    def test_window_task_exists(self):
        childs = (type(i) for i in self.root.winfo_children())
        self.assertIn(tk.Toplevel, childs)
        
    def test_textarea_exists(self):
        top_level = next(i for i in self.root.winfo_children() if isinstance(i, tk.Toplevel))
        top_level_children_types = (type(i) for i in top_level.winfo_children())
        msg = "tk.Toplevel object has no tk.Text for text area"
        self.assertIn(tk.Text, top_level_children_types, msg)
    
    def test_textarea_placeholder(self):
        top_level = next(i for i in self.root.winfo_children() if isinstance(i, tk.Toplevel))
        top_level_children = (i for i in top_level.winfo_children())
        text_area = next(i for i in top_level_children if isinstance(i, tk.Text))
        expected = "Input your note\n"
        msg = 'tk.Text must contain a placeholder "Input your note\n"'

        self.assertEqual(expected, text_area.get(1.0, "end"), msg)
        
    def test_save_button(self):
        top_level = next(i for i in self.root.winfo_children() if isinstance(i, tk.Toplevel))
        top_level_children = (type(i) for i in top_level.winfo_children())
        msg = "tk.Toplevel object has no tk.Button"
        self.assertIn(tk.Button, top_level_children, msg)
        
    def test_save_note_to_csv(self):
        self.root._window_task()
        self.root._save_note()
        frmt = self.root._pattern_time
        start = datetime.now().strftime(frmt)        
        delta = "seconds=5"
        task = "Input your note\n"
        expected = (start, delta, task)
        
        fname = "tasks.csv"
        with open(fname, "r") as file:
                
            reader = csv.reader(file)
            last = next(reader)

            # avoid to create container from generator
            for last in reader: pass
        
            for exp, hav in zip(expected, last):
                with self.subTest(i=exp):
                    self.assertEqual(exp, hav)
                    
        self.remove_tail_csv(start)
        
    def test_save_note_destroy_window_task(self):
        self.root._save_note()
        start = datetime.now().strftime(self.root._pattern_time)
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task mus be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)
        self.remove_tail_csv(start)
    
class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.root = App()
        self.root._general_properties()
        self.root._set_widgets()
        self.root._current_time()
        self.root._check_tasks()
        self.root.dooneevent()
        
    def tearDown(self):
        self.root.destroy()
        
    @staticmethod    
    def remove_tail_csv(start):
        '''Remove last row when during testing function saves information to tasks.csv'''
        
        fname = "tasks.csv"
        fname_temp = "temp.csv"       
    
        with open(fname, "r") as infile, open(fname_temp, "w") as outfile:
            reader = csv.reader(infile)
            header = next(reader)
            writer = csv.writer(outfile, header)
            
            writer.writerow(header)
            writer.writerows(
                takewhile(lambda x: x[0] != start, reader))
    
            os.rename(fname_temp, fname)        
    
    def test_button_task_exists(self):
        but_task = self.root.winfo_children()[-1] ##########
        expected = tk.Button
        self.assertEqual(expected, type(but_task))
        
    def test_button_task_text(self):
        but_task = self.root.winfo_children()[-1]
        expected = "task"
        self.assertEqual(expected, but_task["text"])
        
    def test_create_task_win(self):
        self.root._window_task()
        childs = (type(i) for i in self.root.winfo_children())
        self.assertIn(tk.Toplevel, childs)
        
    def test_save_note_destroy_window_task(self):
        self.root._window_task()
        start = datetime.now().strftime(self.root._pattern_time)
        self.root._save_note()
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task must be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)
        self.remove_tail_csv(start)
                 
    
if __name__ == "__main__":
    unittest.main()
        
        
        
        
        
        
