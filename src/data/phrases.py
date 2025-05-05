from pathlib import Path
from random import sample
from typing import List, Optional


class Phrases:
    def __init__(self, phrases_file: Path) -> None:
        self.phrases = {"Unknown": []}
        self.phrases_file = phrases_file
        self.read_phrases()

    def add_phrase(self, phrase: str) -> None:
        if "©" in phrase:
            author = phrase.split("© ")[-1]
        else:
            author = "Unknown"
        if author in self.phrases.keys():
            self.phrases[author].append(phrase)
        else:
            self.phrases[author] = [phrase]

    def read_phrases(self) -> None:
        phrase = ""
        with open(self.phrases_file, "r", encoding="utf-8") as file:
            for line in file:
                if line == "\n":
                    self.add_phrase(phrase)
                    phrase = ""
                else:
                    phrase += line
        # One more time because it works that way
        self.add_phrase(phrase)

    def exclude_phrases(self, excluded_phrases: 'Phrases') -> bool:
        result = {"Unknown": []}
        phrases_excluded = 0
        for author, phrases in self.phrases.items():
            filtered_phrases = []
            for phrase in phrases:
                if author in excluded_phrases.phrases.keys():
                    if phrase in excluded_phrases.phrases[author]:
                        phrases_excluded += 1
                        continue
                if phrase.split("©")[0] in excluded_phrases.phrases["Unknown"]:
                    print(f"WARNING Add author to phrase in used_moments.txt:\n{phrase}")
                    phrases_excluded += 1
                    continue
                filtered_phrases.append(phrase)
            result[author] = filtered_phrases
        if len(excluded_phrases) == phrases_excluded:
            self.phrases = result
            return True
        else:
            return False

    def exclude_authors(self, authors: List[str]) -> Optional[str]:
        last_author = ""
        try:
            for author in authors:
                last_author = author
                self.phrases.pop(author)
        except KeyError:
            return last_author
        return None

    def get_random_phrases(self, count: int) -> List[str]:
        all_phrases = []
        for _, phrases in self.phrases.items():
            for phrase in phrases:
                all_phrases.append(phrase)
        return sample(all_phrases, count)

    def __len__(self):
        return sum(len(phrases) for _, phrases in self.phrases.items())
