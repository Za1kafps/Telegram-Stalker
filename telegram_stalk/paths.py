import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TargetPaths:
    images: str
    files: str
    voice: str
    log_file: str


def clean_username(username: str) -> str:
    return username.replace("@", "").strip()


def prepare_target_paths(username: str) -> TargetPaths:
    clean = clean_username(username)
    paths = TargetPaths(
        images=f"images-{clean}",
        files=f"files-{clean}",
        voice=f"voice-{clean}",
        log_file=f"log-{clean}.txt",
    )

    for directory in (paths.images, paths.files, paths.voice):
        os.makedirs(directory, exist_ok=True)

    return paths
