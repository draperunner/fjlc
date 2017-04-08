from fjlc.utils import file_utils


class LineReader:

    def __init__(self, file_name):
        self.total_lines = file_utils.count_lines(file_name)
        self.file = open(file_name)
        self.line_counter = 0

    def has_next(self):
        return self.line_counter < self.total_lines

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        self.line_counter += 1
        return self.file.readline()

    def __iter__(self):
        return self

    def get_progress(self):
        return 0 if self.total_lines else 100.0 * self.line_counter / self.total_lines
