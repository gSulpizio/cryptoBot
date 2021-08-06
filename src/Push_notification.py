from notify_run import Notify
import traceback


def push(MSG):
    """Pushes a message to the designated channel
    
    Returns:
        none
    """
    try:
        notify = Notify()
        notify.send(MSG)
    except:
        traceback.print_exc()
        return 0

if __name__ == "__main__":
    push('test')