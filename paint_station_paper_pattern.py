import os
import pygame

PATTERN_WIDTH = 40
PATTERN_HEIGHT = 40
PATTERN_STEP_H = 4
PATTERN_STEP_V = 4

PATTERN_FILE='brush/pattern_{}.png'
PATTERN_COUNT=6

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)

PATTERNS = [
    [(0, 0), (1, 0), (0, 1), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)],
    [(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (3, 3)],
    [(0, 0), (2, 2), (2, 0), (0, 2)],
    [(0, 0), (2, 2)]
]
class PaperPattern():
    def __init__(self):
        self._patterns = []
        self._prepare_patterns()
        self._current_pattern_index = 0

    def _prepare_patterns(self):
        pattern = None

        for pattern_index in range(PATTERN_COUNT):
            pattern_file = PATTERN_FILE.format(pattern_index)
            if os.path.exists(pattern_file):
                pattern = pygame.image.load(pattern_file)
            else:
                pattern = pygame.Surface((PATTERN_WIDTH, PATTERN_HEIGHT))
                if pattern_index == 0:
                    pattern.fill(BLACK)
                elif pattern_index == PATTERN_COUNT - 1:
                    pattern.fill(WHITE)
                else:
                    pattern.fill(WHITE)
                    for i in range(PATTERN_STEP_H // 2, PATTERN_WIDTH, PATTERN_STEP_H):
                        for j in range(PATTERN_STEP_V // 2, PATTERN_HEIGHT, PATTERN_STEP_V):
                            for pos in PATTERNS[pattern_index - 1]:
                                pattern.set_at((i + pos[0], j + pos[1]), BLACK)

                pygame.image.save(pattern, pattern_file)
            self._patterns.append(pattern)

    @property
    def step_h(self):
        return PATTERN_STEP_H

    @property
    def step_v(self):
        return PATTERN_STEP_V

    def get_pattern(self, index=None):
        if index is not None:
            return self._patterns[index]
        else:
            return self._patterns[self._current_pattern_index]

    def set_pattern(self, pattern_index):
        self._current_pattern_index = pattern_index

    @property
    def pattern_2(self):
        return self._pattern_2

    @property
    def pattern_3(self):
        return self._pattern_3

p = PaperPattern()
