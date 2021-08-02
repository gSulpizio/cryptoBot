from notify_run import Notify


def push(MSG):
    """Pushes a message to the designated channel
    
    Returns:
        none
    """
    try:
        notify = Notify()
        notify.send(MSG)
    except:
        return 0

if __name__ == "__main__":
    push('test')