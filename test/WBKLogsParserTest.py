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
        self.assertEqual(6, len(candidates))

    def test_parse_task_name(self):
        name = main.WBKLogsParser.parseTaskName('Graph1')
        self.assertEqual('GRAPH_1', name)

    def test_get_type_name_time(self):
        data = main.WBKLogsParser.readFile('resources/test_plan_2_2.log')
        candidates = main.WBKLogsParser.chooseCandidatesWithTime(data)
        type, name, time = main.WBKLogsParser.getTypeNameTime(candidates[0])
        self.assertEqual((type, name, time), (0, 'GRAPH_3', '2018-03-29 08:58:48'))

    def test_pivot_dependencies(self):
        newPivot = main.WBKLogsParser.reformatRelations([['TASK2', 'TASK1','TASK1']])
        self.assertEqual(newPivot,[['TASK1', 'TASK2']])

    def test_calculate_time(self):
        obj = main.WBKLogsParser.calculateTimes([['task1','2018-03-29 08:58:46','2018-03-29 08:58:48']],[])

        self.assertEqual(obj,[['task1','00:00:02','']])

if __name__ == '__main__':
    unittest.main()