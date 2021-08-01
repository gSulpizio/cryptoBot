from notify_run import Notify


def push(MSG):
    """Pushes a message to the designated channel
    
    Returns:
        none
    """
    notify = Notify()
    notify.send(MSG)

if __name__ == "__main__":
    push('test')