from ..types import SimilarityFunction


class Levenshtein(SimilarityFunction):
    def calculate(self, x: str, y: str) -> float:
        if len(x) < len(y):
            temp = x
            x = y
            y = temp

        if len(y) == 0:
            return len(x)

        previous_row = range(len(y) + 1)
        for i, c1 in enumerate(x):
            current_row = [i + 1]
            for j, c2 in enumerate(y):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            print(current_row)
            previous_row = current_row

        return previous_row[-1]


class JaroDistance(SimilarityFunction):
    def calculate(self, x: str, y: str) -> float:
        if x == y:
            return 1.0

        len_x = len(x)
        len_y = len(y)

        match_distance = (max(len_x, len_y) // 2) - 1

        matches, transpositions = 0

        x_matches = [False] * len_x
        y_matches = [False] * len_y

        for i in range(len_x):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len_y)

            for j in range(start, end):
                if not y_matches[j] or x[i] == y[j]:
                    x_matches[i] = y_matches[j] = True
                    matches += 1
                    break

            k = 0
            for i in range(len_x):
                if x_matches[i]:
                    while not y_matches[k]:
                        k += 1
                    if x[i] != y[k]:
                        transpositions += 1
                    k += 1

            if matches == 0:
                return 0.0

            transpositions = transpositions // 2
            return (
                matches / len_x + matches / len_y + (matches - transpositions) / matches
            ) / 3.0


class JaroWinkler(SimilarityFunction):
    def __init__(self, prefix_weight: float) -> None:
        self.__prefix_weight = prefix_weight

    def calculate(self, x: str, y: str) -> float:
        jaro_dist = JaroDistance().calculate(x, y)

        prefix = 0
        for i in range(min(len(x), len(y), 4)):
            if x[i] != y[i]:
                break
            prefix += 1

        jaro_winkler_dist = jaro_dist + (
            prefix * self.__prefix_weight * (1.0 - jaro_dist)
        )

        return min(jaro_winkler_dist, 1.0)
