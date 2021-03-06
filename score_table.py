import shelve


class ScoreTable:
    def __init__(self, file_path):
        self.entries_count = 8
        self.file_path = file_path
        with shelve.open(file_path) as f:
            if "best_score" not in f:
                f["best_score"] = 0
            if "score_list" not in f:
                f["score_list"] = []
            self.value = f["best_score"]
            self.scores = f["score_list"]

    def update_score(self, value, player_name):
        with shelve.open(self.file_path) as f:
            if value > self.value:
                self.value = value
                f["best_score"] = value

            self.scores.append((player_name, value))
            self.scores = sorted(self.scores, key=lambda x: x[1], reverse=True)
            if len(self.scores) > self.entries_count:
                self.scores.pop()
            f["score_list"] = self.scores
