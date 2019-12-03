import inspect
import os

def get_puzzle_input(puzzle = None, puzzle_input_folder = None):
    if puzzle is None:
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        puzzle = os.path.splitext(os.path.basename(filename))[0]

    if puzzle_input_folder is None:
        puzzle_input_folder = os.path.join(os.path.dirname(__file__),
                                           'puzzle_inputs')

    filename = os.path.join(puzzle_input_folder, puzzle+'.txt')
    with open(filename) as f:
        return f.read()
