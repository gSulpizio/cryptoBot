from notify_run import Notify


def push(MSG):
    notify = Notify()
    notify.send(MSG, 'https://notify.run/xd6BvS3LEQwP5vNH')

if __name__ == "__main__":
    push('test')