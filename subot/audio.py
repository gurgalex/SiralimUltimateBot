import enum
from dataclasses import dataclass
from enum import auto
from typing import Optional

import pygame
import win32com.client

from subot.utils import Point


@dataclass
class AudioLocation:
    distance: Point


Left = float
Right = float


def volume_from_distance(distance: Point) -> tuple[Left, Right]:
    if distance.x > 0:
        return Left(0), \
               Right(1 / (distance.x + 1 + abs(distance.y)))
    elif distance.x < 0:
        return Left(1 / (abs(abs(distance.x) + abs(distance.y)) + 1)), \
               Right(0)
    else:
        return Left(1 / (abs(distance.y) + 1)), \
               Right(1 / (abs(distance.y) + 1))


class SoundType(enum.Enum):
    QUEST_ITEM = auto()
    MASTER_NPC = auto()
    NPC_NORMAL = auto()
    ALTAR = auto()
    PROJECT_ITEM = auto()


@dataclass
class SoundIndicator:
    low: pygame.mixer.Sound
    normal: pygame.mixer.Sound
    high: pygame.mixer.Sound


@dataclass
class SoundMapping:
    channel: pygame.mixer.Channel
    sounds: SoundIndicator


class AudioSystem:
    def __init__(self):

        self.sound_mappings: dict[SoundType, SoundMapping] = {
            SoundType.ALTAR: SoundMapping(
                channel=pygame.mixer.Channel(2),
                sounds=SoundIndicator(
                    low=pygame.mixer.Sound("../audio/altar-angel-low.ogg"),
                    normal=pygame.mixer.Sound("../audio/altar-angel-normal.ogg"),
                    high=pygame.mixer.Sound("../audio/altar-angel-high.ogg"),
                )
            ),

            SoundType.MASTER_NPC: SoundMapping(
                channel=pygame.mixer.Channel(5),
                sounds=SoundIndicator(
                    low=pygame.mixer.Sound("../audio/horse_sound_cc0-low.wav"),
                    normal=pygame.mixer.Sound("../audio/horse_sound_cc0.wav"),
                    high=pygame.mixer.Sound("../audio/horse_sound_cc0-high.wav"),
                )
            ),

            SoundType.NPC_NORMAL: SoundMapping(
                channel=pygame.mixer.Channel(4),
                sounds=SoundIndicator(
                    low=pygame.mixer.Sound("../audio/npc-low.ogg"),
                    normal=pygame.mixer.Sound("../audio/npc-normal.ogg"),
                    high=pygame.mixer.Sound("../audio/npc-high.ogg"),
                )
            ),

            SoundType.PROJECT_ITEM: SoundMapping(
                channel=pygame.mixer.Channel(3),
                sounds=SoundIndicator(
                    low=pygame.mixer.Sound("../audio/project-item-low.ogg"),
                    normal=pygame.mixer.Sound("../audio/project-item-normal.ogg"),
                    high=pygame.mixer.Sound("../audio/project-item-high.ogg"),
                )
            ),

            SoundType.QUEST_ITEM: SoundMapping(
                channel=pygame.mixer.Channel(0),
                sounds=SoundIndicator(
                    low=pygame.mixer.Sound("../audio/tone-low.wav"),
                    normal=pygame.mixer.Sound("../audio/tone-normal.wav"),
                    high=pygame.mixer.Sound("../audio/tone-high.wav"),
                )
            ),

        }

        # Windows TTS speaker
        self.Speaker = win32com.client.Dispatch("SAPI.SpVoice")
        # don't block the program when speaking. Cancel any pending speaking directions
        self.SVSFlag = 3  # SVSFlagsAsync = 1 + SVSFPurgeBeforeSpeak = 2
        self.Speaker.Voice = self.Speaker.getVoices('Name=Microsoft Zira Desktop').Item(0)

    def play_sound(self, audio_tile: AudioLocation, sound_type: SoundType):
        distance_y = audio_tile.distance.y

        sound_mapping = self.sound_mappings[sound_type]
        channel = sound_mapping.channel

        if distance_y > 0:
            sound = sound_mapping.sounds.low
        elif distance_y < 0:
            sound = sound_mapping.sounds.high
        else:
            sound = sound_mapping.sounds.normal

        volume = volume_from_distance(audio_tile.distance)
        if channel.get_sound() != sound:
            channel.play(sound, -1)
            channel.set_volume(*volume)

        channel.set_volume(*volume)

    def stop(self, sound_type: SoundType):
        self.sound_mappings[sound_type].channel.stop()
