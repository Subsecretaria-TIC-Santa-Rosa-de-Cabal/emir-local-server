from dataclasses import dataclass


@dataclass
class SaveFileResponseDTO:
    absolute_path: str
