from tkinter.ttk import LabelFrame
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
from taskwindow import TaskWindow
from savetask import SaveTask
from colors import COLORS
from tasklist import TaskList

import typing as tp

# @unittest.skip
class TestGlobal(unittest.TestCase):
    
    def setUp(self):
        '''Create new test base, the main base is renamed'''

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
    
    def test_save_task(self):
        pattern_time = '%Y-%m-%d %H:%M:%S'
        task =  f"text for dev purposes: {os.path.basename(__file__)}"
        start_str = datetime.now().strftime(pattern_time)
        
        SaveTask._save_task(start_str, task)
        
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
        self.win_dt = DateTimeWindow()
        self.win_dt.task = "text for dev purposes"
        self.win_dt._init_win_dt(self.win_dt.task)
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


# @unittest.skip        
class TestTaskWindow(TestGlobal):

    def setUp(self):
        super().setUp()
        self.root = tk.Tk()
        self.task = "text for test purpose"
        scheme = "deep blue"
        TaskWindow(self.task, scheme)    

    def tearDown(self):
        self.root.destroy()
        
    def test_window_task_exists(self):
        obj = self.root.winfo_children()[0]
        self.assertIsInstance(obj, tk.Toplevel)
        
    def test_textarea_exists(self):
        toplevel = self.root.winfo_children()[0]
        textarea = toplevel.winfo_children()[0]
        msg = "Toplevel object has no Text object"
        self.assertIsInstance(textarea, tk.Text, msg)
            
    def test_task_text(self):
        toplevel = self.root.winfo_children()[0]
        textarea = toplevel.winfo_children()[0]
        task = textarea.get(1.0, "end")     # type: ignore
        expected = self.task + "\n"
        self.assertEqual(expected, task)

    def test_textarea_colorscheme(self):
        toplevel = self.root.winfo_children()[0]
        textarea = toplevel.winfo_children()[0]
        bg = textarea["bg"]
        expected = "#89EBEB"
        self.assertEqual(expected, bg)

    def test_remind_buttons(self):
        top_level = next(el for el in self.root.winfo_children() if isinstance(el, tk.Toplevel))
        frames = [el for el in top_level.winfo_children() if isinstance(el, tk.Frame)]
        button_texts = [el["text"] for frame in frames for el in frame.winfo_children() if isinstance(el, tk.Button)]

        for delta in ["15 min", "1.5 hour", "1 day", "random", "choose", "end task"]:
            with self.subTest(i=delta):
                msg = f"tk.Toplevel object has no button with {delta}"
                self.assertIn(delta, button_texts, msg)

        
class TestTaskList(TestGlobal):

    def setUp(self):
        super().setUp()

        pattern_time = '%Y-%m-%d %H:%M:%S'
        
        for i, delta in enumerate((0, 0, 1)):
            task =  f"text {delta}"
            start = datetime.now() + timedelta(days=delta)
            SaveTask._save_task(start.strftime(pattern_time), task)
        
        fname = "tasks.csv"
        scheme = "deep blue"
        self.task_list = TaskList(fname, scheme)

    def tearDown(self):
        self.task_list.destroy()
        
    def test_task_list_exists(self):
        self.assertIsInstance(self.task_list, tk.Toplevel)
        
    def test_nubmer_buttons(self):
        buttons = [i for i in self.task_list.winfo_children() if isinstance(i, tk.Button)]
        msg = "There wrong number of buttons on TaskList obj"
        self.assertEqual(1, len(buttons), msg)

    def test_suited_buttons_exists(self):
        buttons = (i for i in self.task_list.winfo_children() if isinstance(i, tk.Button))
        expected = ("OK",)

        for exp, real in zip(expected, buttons):
            with self.subTest(i=exp):
                self.assertEqual(exp, real["text"])

    def test_tasks_exists(self):
        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        frames = [el.winfo_children()[0] for el in childs if isinstance(el, tk.Frame)]
        
        expected: int = 2
        msg: str = f"Wrong number of Frames objs (tasks), expected {expected}"
        existed: int = len(frames)

        self.assertEqual(expected, existed, msg)

    def test_entries_exists(self):
        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        entries = [el.winfo_children()[1] for el in childs if isinstance(el, tk.Frame)]
        
        expected: int = 2
        msg: str = f"Wrong number of Entry objs, expected {expected}"
        existed: int = len(entries)

        self.assertEqual(expected, existed, msg)
            
    def test_entries_content(self):
        """check TaskList chooses today's entries"""

        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        entries = (el.winfo_children()[0] for el in childs if isinstance(el, tk.Frame))
        existed_texts = (entry.get() for entry in entries)    # type: ignore

        task: str = "text 0"
        start_str: str = datetime.now().strftime("%H:%M")
        expected_texts: tp.Tuple[str, ...] = (task,)*2 

        for exp, real in zip(expected_texts, existed_texts):
            with self.subTest(i=exp):
                self.assertEqual(exp, real)

    def test_entry_bg_colorscheme(self):
        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        entries = (el.winfo_children()[0] for el in childs if isinstance(el, tk.Frame))
        existed_colors = (entry["bg"] for entry in entries)

        expected_color = "#89EBEB"

        for color in existed_colors:

            with self.subTest(i=color):
                self.assertEqual(expected_color, color)

    def test_entry_fg_colorscheme(self):

        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        entries = (el.winfo_children()[0] for el in childs if isinstance(el, tk.Frame))
        existed = (entry["fg"] for entry in entries)

        expected = "#000000"

        for color in existed:

            with self.subTest(i=color):
                self.assertEqual(expected, color)
            
    def test_labels_exists(self):
        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        labels = [el.winfo_children()[1] for el in childs if isinstance(el, tk.Frame)]
        
        expected: int = 2
        msg: str = f"Wrong number of Entry objs, expected {expected}"
        existed: int = len(labels)

        self.assertEqual(expected, existed, msg)
            
    def test_labels_content(self):
        """check TaskList chooses today's labels (label_times)"""

        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        labels = (el.winfo_children()[1] for el in childs if isinstance(el, tk.Frame))
        existed: tp.Generator = (label["text"] for label in labels)    # type: ignore

        start_str: str = datetime.now().strftime("%H:%M")
        expected: tp.Tuple[str, ...] = (start_str,)*2 

        for exp, real in zip(expected, existed):
            with self.subTest(i=exp):
                self.assertEqual(exp, real)

    def test_label_bg_colorscheme(self):
        childs: tp.List[tk.Widget] = self.task_list.winfo_children()
        labels = (el.winfo_children()[1] for el in childs if isinstance(el, tk.Frame))
        existed_colors = (entry["bg"] for entry in labels)

        expected_color = "#062656"

        for color in existed_colors:

            with self.subTest(i=color):
                self.assertEqual(expected_color, color)


# @unittest.skip
class TestDB(TestGlobal):
        
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


        
# @unittest.skip    
class TestApp(TestGlobal):
    
    def setUp(self):
        super().setUp()
        self.root = App()
        self.root.dooneevent()
    
    def tearDown(self):
        self.root.destroy()
    
    def test_button_task_exists(self):
        but_task = self.root.winfo_children()[-1]
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
        
    # def test_save_task_destroy_window_task(self):
    #     task_window = TaskWindow()
    #     task_window._init_win_task()
    #     task_window._end_task()
    #     childs = (type(i) for i in self.root.winfo_children())
    #     msg = "After saving the window task must be destroyed"
    #
    #     import pdb; pdb.set_trace()
    #     self.assertNotIn(tk.Toplevel, childs, msg)

# @unittest.skip
class Test2App(TestGlobal):
    """Test check proper text of task in Task Window"""
    
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


# @unittest.skip        
class TestColorDeepBlue(unittest.TestCase):
    
    def setUp(self): 
        self.root = tk.Tk()
        scheme = COLORS["deep blue"]

        tk.Button(self.root, text="test Button", **scheme["button"]).pack()

        entry_task = tk.Entry(self.root, **scheme["entry_task"])
        entry_task.insert(0, "test Entry")
        entry_task.pack()

        tk.Label(self.root, text="test LabelTime", **scheme["label_time"])
        self.root.dooneevent()
        
    def tearDown(self):
        self.root.destroy()
            
    def test_button_color(self):
        childs: list[tk.Widget] = self.root.winfo_children()
        button: tk.Button = next(but for but in childs if isinstance(but, tk.Button))
        
        expected_vals = ("#062656", "#4FC500","#4FC500","#38418A")
        real_vals: tp.Iterable[str] = (button["bg"], button["fg"], button["activeforeground"], button["activebackground"])
        msg = "Improper color scheme of Button"
        
        for exp, real in zip(expected_vals, real_vals):
            
            with self.subTest(i=exp):
                self.assertEqual(exp, real, msg)

    def test_entry_task_color(self):
        childs: list[tk.Widget] = self.root.winfo_children()
        entry: tk.Entry = next(
                el for el in childs if isinstance(el, tk.Entry)
                )
        
        expected_vals = ("#89EBEB", "#000000")
        real_vals: tp.Iterable[str] = (entry["bg"], entry["fg"])
        msg = "Improper color scheme of Entry"
        
        for exp, real in zip(expected_vals, real_vals):
            
            with self.subTest(i=exp):
                self.assertEqual(exp, real, msg)                

    def test_label_time_color(self):

        childs: list[tk.Widget] = self.root.winfo_children()
        label_time: tk.Label = next(
                el for el in childs if isinstance(el, tk.Label)
                )
        
        expected_vals = ("#062656", "#4FC500")
        real_vals = (label_time["bg"], label_time["fg"])
        msg = "Improper color scheme of LabelTime"
        
        for exp, real in zip(expected_vals, real_vals):
            
            with self.subTest(i=exp):
                self.assertEqual(exp, real, msg)                
            

if __name__ == "__main__":
    unittest.main()

