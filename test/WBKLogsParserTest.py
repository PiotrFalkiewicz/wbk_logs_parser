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



class TestSecondIteration(unittest.TestCase):
    def test_read_CSV_file(self):
        data = main.WBKLogsParser.readCSVFile('resources/test_plan_2_1.log')
        self.assertEqual(4, len(data))

    def test_candidates_with_time(self):
        data = main.WBKLogsParser.readFile('resources/test_plan_2_2.log')
        candidates = main.WBKLogsParser.chooseCandidatesWithTime(data)
        self.assertEqual(8, len(candidates))

    def test_parse_task_name(self):
        name = main.WBKLogsParser.parseTaskName('Graph1')
        self.assertEqual('GRAPH_1', name)

    def test_get_type_name_time(self):
        data = main.WBKLogsParser.readFile('resources/test_plan_2_2.log')
        candidates = main.WBKLogsParser.chooseCandidatesWithTime(data)
        type, name, time = main.WBKLogsParser.getTypeNameTime(candidates[0])
        self.assertEqual((type, name, time), (0, 'GRAPH_3', '32326'))

if __name__ == '__main__':
    unittest.main()