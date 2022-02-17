import psutil

from .watchlist import WatchList
from .notifications import notify


def find_finished_pids(pid_file):
    """Find finished pids in pid_file """
    watch_list = WatchList()
    watch_list.from_json(pid_file)

    done = []
    for entry in watch_list:
        if psutil.pid_exists(entry.pid):
            # pid assigned to new process
            if psutil.Process(entry.pid).name() != entry.name:
                done.append(entry)
        else:
            # pid has finished
            done.append(entry)

    # only remove entries after iterating
    done = set(done)
    for entry in done:
        watch_list.remove(entry)
        watch_list.to_json(pid_file)

    return done


def check_pids(config):
    """Notify for all finished pids in pid_file."""
    finished = find_finished_pids(config["pid_file"])
    if len(finished) > 0:
        for entry in finished:
            notify(entry, config)
