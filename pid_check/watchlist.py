from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Set


@dataclass
class Entry:
    """Class for PID entries to check status off"""
    pid: int
    name: str
    method: str

    def __hash__(self):
        return hash(
            (
                self.pid,
                self.name,
                self.method,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise NotImplementedError(f"Cannot compare {type(self)} to {type(other)}")

        return (
            (self.pid == other.pid)
            & (self.name == other.name)
            & (self.method == other.method)
        )


@dataclass
class WatchList:
    """List of Entry objects"""
    entries: Set[Entry] = field(default_factory=set)

    def clear(self):
        self.entries = set()

    def add(self, entry):
        if entry not in self.entries:
            self.entries.add(entry)

    def remove(self, entry):
        if entry in self.entries:
            self.entries.remove(entry)

    def __iter__(self):
        for entry in self.entries:
            yield entry

    def to_json(self, fname):
        entries_list = []
        for entry in self.entries:
            entries_list.append(entry.__dict__)

        with open(fname, "w") as f:
            json.dump(entries_list, f)

    def from_json(self, fname):
        if Path(fname).exists():
            with open(fname, "r") as f:
                entries_list = json.load(f)

            for entry_dict in entries_list:
                entry = Entry(**entry_dict)
                if entry not in self.entries:
                    self.entries.add(entry)
