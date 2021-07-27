from notify_run import Notify


def push(MSG):
    notify = Notify()
    notify.send(MSG)

if __name__ == "__main__":
    push('test')