import main.WBKLogsParser

import unittest


class TestFirstIteration(unittest.TestCase):
    def test_read_file(self):
        data = main.WBKLogsParser.readFile('resources/test_plan.log')
        self.assertEqual(len(data), 4)

    def test_candidates(self):
        data = main.WBKLogsParser.readFile('resources/test_plan.log')
        candidates = main.WBKLogsParser.chooseCandidates(data)
        self.assertEqual(len(candidates), 2)

    def test_mining_names(self):
        data = main.WBKLogsParser.readFile('resources/test_plan.log')
        candidates = main.WBKLogsParser.chooseCandidates(data)
        names = main.WBKLogsParser.parseLinesToNames(candidates)
        self.assertEqual(names[0], 'GRAPH_TASK1')

    def test_select_names_distinct(self):
        data = main.WBKLogsParser.readFile('resources/test_plan.log')
        candidates = main.WBKLogsParser.chooseCandidates(data)
        names = main.WBKLogsParser.parseLinesToNames(candidates)
        distinctNames = main.WBKLogsParser.utilDistinct(names)
        self.assertEqual(len(distinctNames), 1)

    def test_final_collection(self):
        data = main.WBKLogsParser.readFile('resources/test_plan.log')
        candidates = main.WBKLogsParser.chooseCandidates(data)
        names = main.WBKLogsParser.parseLinesToNames(candidates)
        distinctNames = main.WBKLogsParser.utilDistinct(names)
        self.assertEqual(distinctNames, ['GRAPH_TASK1'])

if __name__ == '__main__':
    unittest.main()