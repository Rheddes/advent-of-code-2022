import unittest
import coordinates


class CoordinatesTest(unittest.TestCase):
    def test_can_generate_range_of_y_coordinates(self):
        start = coordinates.Point(0, 1)
        end = coordinates.Point(0, 4)
        generated = [coord for coord in coordinates.move_straight(start, end)]
        self.assertEqual(generated, [coordinates.Point(0, 1), coordinates.Point(0, 2), coordinates.Point(0, 3)])

    def test_can_generate_range_of_x_coordinates(self):
        start = coordinates.Point(1, 0)
        end = coordinates.Point(3, 0)
        generated = [coord for coord in coordinates.move_straight(start, end)]
        self.assertEqual(generated, [coordinates.Point(1, 0), coordinates.Point(2, 0)])

    def test_can_create_point_from_string(self):
        p = coordinates.point_from_string('2,1')
        self.assertEqual(coordinates.Point(2, 1), p)


if __name__ == '__main__':
    unittest.main()
