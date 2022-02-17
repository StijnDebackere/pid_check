from dataclasses import dataclass, field
import datetime
from pathlib import Path
import os
import subprocess
from textwrap import dedent


@dataclass
class Message:
    subject: str
    message: str


def get_message(entry):
    now = datetime.datetime.now()
    hostname = os.uname().nodename

    subject = f"[pid_check] Finished {entry.name} on {hostname}"
    message = f"""\
    Hi,

    Process-{entry.pid} -- {entry.name} on {hostname}
    has finished at {now}.

    Bye!
    """
    return Message(subject=subject, message=message)


def notify_email(entry, config):
    """Send email notification about entry.

    Parameters
    ----------
    entry : Entry
    config : dict
        'email_address': email to send to
    """
    msg = get_message(entry)

    temp_fname = f"/var/tmp/pid-check-{hash(entry)}.txt"
    with open(temp_fname, "w") as f:
        f.write(dedent(msg.message))


    cat = subprocess.Popen(["cat", temp_fname], stdout=subprocess.PIPE)
    subprocess.Popen(
        [
            "mail",
            "-s",
            msg.subject,
            config["email_address"],
        ],
        stdin=cat.stdout,
        env=os.environ,
    )
    Path(temp_fname).unlink(missing_ok=True)


def notify(entry, config):
    if entry.method == "email":
        notify_email(entry, config=config["method"]["email"])
