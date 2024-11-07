import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import json

BASE_URL = "http://localhost:8000"


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file uploaded: {event.src_path}")
            self.perform_action(event.src_path)

    def perform_action(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            # ___ 1
            content = file.read()
            payload = {"text": content}
            url = f"{BASE_URL}/extract-data"
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            # ___ 2
            payload.pop("text")
            payload["data"] = response.json()
            url = f"{BASE_URL}/evaluate-property"
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            # ___ 3
            payload["estimated_value"] = response.json()
            url = f"{BASE_URL}/check-solvency"
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            # ___ 4
            payload = {}
            payload["client_solvable"] = response.json()
            url = f"{BASE_URL}/make-decision"
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
            )
            print(response.json())


def start_watching(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    folder_to_watch = "TP_FAST_API/demands"
    start_watching(folder_to_watch)
