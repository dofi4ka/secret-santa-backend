from typing import Hashable
from random import choice


class ParticipiantHasNoOptions(ValueError):
    def __init__(self, participiant):
        self.participiant = participiant


def distribution_with_banlist[T: Hashable](participiants: dict[T, set[T]]) -> dict[T, T]:
    distributed = {}
    data = set(participiants.keys())
    while participiants:
        participiant = max(participiants, key=lambda key: len(participiants[key]))
        available_options = tuple(data - participiants[participiant])
        if not available_options:
            raise ParticipiantHasNoOptions(participiant=participiant)
        chosen_options = choice(available_options)
        distributed[participiant] = chosen_options
        del participiants[participiant]
        for banlist in participiants.values():
            banlist.add(chosen_options)
    return distributed


__all__ = ["distribution_with_banlist", "ParticipiantHasNoOptions"]
