class ImageResult(object):
    def __init__(self):
        self.matches = []
        self.false_positives = []
        self.unrecognized = []

    def add_match(self, box1, box2):
        self.matches.append((box1, box2))

    def add_false_positive(self, box):
        self.false_positives.append(box)

    def add_unrecognized(self, box):
        self.unrecognized.append(box)

    def n_matches(self):
        return len(self.matches)

    def n_false_positives(self):
        return len(self.false_positives)

    def n_unrecognized(self):
        return len(self.unrecognized)


class DataSetResult(object):
    def __init__(self):
        self.images_results = []
        self.n_matches = 0
        self.n_false_positives = 0
        self.n_unrecognized = 0

    def add_image_result(self, result):
        self.images_results.append(result)
        self.n_matches += result.n_matches()
        self.n_false_positives = result.n_false_positives()
        self.n_unrecognized += result.n_unrecognized()

    def __str__(self):
        return "DataSetResult : %d matches, %d false positive, %d missed"%(self.n_matches,
                                                                           self.n_false_positives,
                                                                           self.n_unrecognized)
