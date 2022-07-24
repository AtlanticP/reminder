# These classes were made only for test purposes
class DummyGetTask:
    
    def get(self, *args, **kwargs) -> str:
        return "text for dev purposes"
    
    def destroy(self, *args, **kwargs) -> None:
        pass

class DummyClass: 
    
    txt_task = DummyGetTask()
    win_task = DummyGetTask()

