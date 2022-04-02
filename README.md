# `pid_check`
Simple tool to send notifications when watched processes finish running.

# Installation
Install the library by typing
```
git clone https://github.com/StijnDebackere/pid_check
cd pid_check
pip install -e .
```

# Usage
Start the background daemon by running
```
watchpids
```
Now you can add any long-running processes to the watchlist by invoking
```
addpid PID0 PID1 ...
```
This will log the running process in the `pid_file` specified in the toml [configuration file](https://github.com/StijnDebackere/pid_check/blob/main/pid_check/config.toml#L1=). The configuration file also specifies the `check_interval` (in seconds) for the daemon to check which processes are running.

Currently, when a watched process terminates, `pid_check` sends an email to the email address specified in the [configuration file](https://github.com/StijnDebackere/pid_check/blob/main/pid_check/config.toml#L6=)
