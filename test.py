import unittest
import tkinter as tk
from datetime import datetime, timedelta
from itertools import takewhile
import os
import shutil
import time
import csv

from main import App
from task import TaskWindow
#%%
# @unittest.skip
class TestGlobal(unittest.TestCase):
    
    def setUp(self):
        '''Create new test base, the main base is renamed'''
        
        self.fname = "tasks.csv"
        self.fname_temp = "task_test.csv"
        shutil.copy(self.fname, self.fname_temp)
        os.remove(self.fname)
        
    def tearDown(self):
        '''recover main base'''
        
        os.rename(self.fname_temp, self.fname)
        self.root.destroy()

# @unittest.skip        
class TestTaskWindow(TestGlobal):

    def setUp(self):
        super().setUp()
        self.root = TaskWindow()
        self.root._window_task()
        
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
        
    def test_remind_buttons(self):
        top_level = next(el for el in self.root.winfo_children() if isinstance(el, tk.Toplevel))
        button_texts = (el["text"] for el in top_level.winfo_children() if isinstance(el, tk.Button))

        for delta in ["15 min", "1.5 hour"]:
            with self.subTest(i=delta):
                msg = f"tk.Toplevel object has no button with {delta}"
                self.assertIn(delta, button_texts, msg)
            
    def test_save_note_to_csv(self):
        self.root._window_task()
        delta = "seconds=5"
        self.root._save_note(delta)
        frmt = self.root._pattern_time
        start = datetime.now().strftime(frmt)        
        
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
        
    def test_save_note_destroy_window_task(self):
        delta = "seconds=5"
        self.root._save_note(delta)
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task mus be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)
    
class TestApp(TestGlobal):
    
    def setUp(self):
        super().setUp()
        self.root = App()
        self.root.dooneevent()
    
    def test_button_sched_exists(self):
        but_task = self.root.winfo_children()[-1] ##########
        expected = tk.Button
        self.assertEqual(expected, type(but_task))
        
    def test_button_sched_text(self):
        but_task = self.root.winfo_children()[-1]
        expected = "task"
        self.assertEqual(expected, but_task["text"])
        
    def test_create_task_win(self):
        self.root._window_task()
        childs = (type(i) for i in self.root.winfo_children())
        self.assertIn(tk.Toplevel, childs)
        
    def test_save_note_destroy_window_task(self):
        self.root._window_task()
        delta = "seconds=5"
        self.root._save_note(delta)
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task must be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)

# @unittest.skip
class Test2App(TestGlobal):
    
    def setUp(self):
        super().setUp()
        fname = "tasks.csv"
        pattern_time = "%Y-%m-%d %H:%M:%S"
        
        with open(fname, "a") as file:
            fieldnames = ["start", "delta", "task"]
            writer = csv.DictWriter(file, fieldnames)
            
            start = datetime.now().strftime(pattern_time)
            delta = "milliseconds=10"
            task = "Test in test_check_tasks"
            
            writer.writeheader()            
            writer.writerow({"start": start, "delta": delta, "task": task})                 
        
        self.root = App()
        self.root.fname = "tasks.csv"
        self.task = task
        self.root.dooneevent()
        
    def test_check_tasks(self):

        is_proper_task = False

        for el in self.root.winfo_children():
            if isinstance(el, tk.Toplevel):
                
                for subel in el.winfo_children():
                    if isinstance(subel, tk.Text):
                        # print(subel.get(1.0, "end"))
                        if subel.get(1.0, "end") == self.task + "\n":
                            is_proper_task = True
                            break

                if is_proper_task:
                    break

        msg = "_check_tasks does not raise tk.Toplevel or there not proper text"
        self.assertTrue(is_proper_task, msg)        
        
            
if __name__ == "__main__":
    unittest.main()
        
        
        
        
        
        
