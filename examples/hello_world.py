from datetime import timedelta

from tau.core.api import Event
from tau.core.singlethreaded import SingleThreadedTimeline


class HelloWorld(Event):
    def on_raise(self) -> bool:
        print("Hello, world!")
        return False


timeline = SingleThreadedTimeline()
timeline.run()

timeline.raise_event_after(HelloWorld(), timedelta(seconds=5))

