import unittest
import tkinter as tk
from datetime import datetime, timedelta
import os
import shutil
import csv
from tkcalendar import Calendar
from tktimepicker import AnalogPicker

from picker import DateTimeWindow
from main import App
from task import TaskWindow
from save_task import DummySaveTask
from picker import DummyDateTimeWindow
#%%
# @unittest.skip
class TestGlobal(unittest.TestCase):
    
    def setUp(self):
        '''Create new test base, the main base is renamed'''
        # import pdb; pdb.set_trace()
        self.fname = "tasks.csv"
        
        if os.path.isfile(self.fname):

            self.fname_temp = "task_test.csv"
            shutil.copy(self.fname, self.fname_temp)
            os.remove(self.fname)
            
        with open(self.fname, "w") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(["start", "task"])
                
    def tearDown(self):
        '''recover main base'''
        
        os.rename(self.fname_temp, self.fname)


# @unittest.skip
class TestSaveTask(TestGlobal):
    
    def setUp(self):
        super().setUp()

    def test_save_task(self):
        pattern_time = '%Y-%m-%d %H:%M:%S'
        start_str = datetime.now().strftime(pattern_time)
        DummySaveTask()._save_task(start_str)
        
        task = "text for dev purposes"
        expected = (start_str, task) 
        
        with open(self.fname, "r") as file:
            
            reader = csv.reader(file)
            next(reader)    # header
            
            # to avoid create container            
            for last in reader: pass
            
            for exp, real in zip(expected, last):
                with self.subTest(i=exp):
                    self.assertEqual(exp, real)


# @unittest.skip
class TestDateTimeWindow(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.win_dt = DummyDateTimeWindow()
        self.win_dt.text = "text for dev purposes"
        self.win_dt._win_task()
        self.root.dooneevent()
        
    def tearDown(self):
        self.root.destroy()
        
    def test_calendar_obj_exists(self):
        toplevel = next(el for el in self.root.winfo_children() if isinstance(el, tk.Toplevel)) 
        obj_types = (type(el) for el in toplevel.winfo_children())
        self.assertIn(Calendar, obj_types)
    
    def test_time_obj_exists(self):
        toplevel = next(el for el in self.root.winfo_children() if isinstance(el, tk.Toplevel)) 
        obj_types = (type(el) for el in toplevel.winfo_children())
        self.assertIn(AnalogPicker, obj_types)
        
    def test_button_exists(self):
        toplevel = next(el for el in self.root.winfo_children() if isinstance(el, tk.Toplevel)) 
        obj_types = (type(el) for el in toplevel.winfo_children())
        self.assertIn(tk.Button, obj_types)

@unittest.skip        
class TestTaskWindow(TestGlobal):

    def setUp(self):
        super().setUp()
        self.root = TaskWindow()
        self.root._window_task()
    
    def tearDown(self):
        self.root.destroy()
        
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
            
    def test_save_task_to_csv(self):
        self.root._window_task()
        now = datetime.now()
        params = {"seconds": 5}
        delta = timedelta(**params)
        start_str = (now + delta).strftime(self.root._pattern_time)

        self.root._save_task(start_str)
        
        task = "Input your note\n"
        expected = (start_str, task)
        
        fname = "tasks.csv"
        with open(fname, "r") as file:
                
            reader = csv.reader(file)
            last = next(reader)

            # avoid to create container from generator
            for last in reader: pass
        
            for exp, hav in zip(expected, last):
                with self.subTest(i=exp):
                    self.assertEqual(exp, hav)
        
    def test_save_task_destroy_window_task(self):
        start = datetime.now().strftime(self.root._pattern_time)
        self.root._save_task(start)
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task mus be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)

@unittest.skip
class TestDB(unittest.TestCase):
        
    def setUp(self):
        self.fname = "tasks.csv"
        self.root = App()
                
    def tearDown(self):
        self.root.destroy()
        
    def test_DB_exists(self):
        msg = 'App must create "tasks.csv"'
        self.assertTrue(os.path.isfile(self.fname), msg)

    def test_DB_contains(self):
        msg = '"tasks.csv first row (header) must be "start,task"'
        expected = "start,task\n"
        
        with open(self.fname, "r") as file:
            text = file.read()
            self.assertEqual(expected, text, msg)
    
@unittest.skip    
class TestApp(TestGlobal):
    
    def setUp(self):
        super().setUp()
        self.root = App()
        self.root.dooneevent()
    
    def tearDown(self):
        self.root.destroy()
    
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
        
    def test_save_task_destroy_window_task(self):
        self.root._window_task()
        self.root._save_task("")
        childs = (type(i) for i in self.root.winfo_children())
        msg = "After saving the window task must be destroyed"
        self.assertNotIn(tk.Toplevel, childs, msg)

@unittest.skip
class Test2App(TestGlobal):
    
    def setUp(self):
        super().setUp()
        fname = "tasks.csv"
        pattern_time = "%Y-%m-%d %H:%M:%S"
        
        now = datetime.now()
        delta = timedelta(milliseconds=10)
        start_str = (now + delta).strftime(pattern_time)
        task = "Test in test_check_tasks"        
        
        with open(fname, "a") as file:
            fieldnames = ["start", "task"]
            writer = csv.DictWriter(file, fieldnames)

            writer.writeheader()            
            writer.writerow({"start": start_str, "task": task})                 
        
        self.root = App()
        self.root.fname = "tasks.csv"
        self.task = task
        self.root.dooneevent()
        
    def tearDown(self):
        self.root.destroy()
        
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

