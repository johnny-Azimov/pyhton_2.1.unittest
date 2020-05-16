import unittest
from unittest.mock import patch
import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.dirs, self.docs = app.update_date()
        with patch('app.update_date', return_value = (self.dirs, self.docs)):
            with patch('app.input', return_value='q'):
                app.secretary_program_start()

    def test_delete(self):
        before_len = len(self.docs)
        with patch('app.input', return_value='11-2'):
            app.delete_doc()
        self.assertLess(len(self.docs), before_len)

    def test_add(self):
        before_len = len(self.docs)
        with patch('app.input', size_effect=['11-3', 'passport', 'test user', '1']):
            app.add_new_doc()
        self.assertGreater(len(self.docs), before_len)

    def test_check_doc_existance(self):
        self.assertTrue(app.check_document_existance('10006'))

    def test_check_all_doc_owners_names(self):
        self.assertEqual(len(set([x['name'] for x in self.docs])), \
        len(app.get_all_doc_owners_names()))

    def test_remove_doc_from_shelf(self):
        before_len = len(self.dirs['2'])
        app.remove_doc_from_shelf('10006')
        self.assertLess(len(self.dirs['2']), before_len)

    def test_add_new_shelf(self):
        before_len = len(self.dirs.keys())
        with patch('app.input', return_value='test'):
            app.add_new_shelf()
        self.assertGreater(len(self.dirs), before_len)

    def test_append_doc_to_shelf(self):
        app.append_doc_to_shelf('111', '3')
        self.assertEqual(self.dirs['3'][-1], '111')

    def test_get_doc_shelf(self):
        with patch('app.input', return_value='11-2'):
            self.assertEqual(app.get_doc_shelf(), '1')

    def test_move_doc_to_shelf(self):
        before_from = len(self.dirs['2'])
        before_to = len(self.dirs['3'])
        with patch('app.input', side_effect=['10006', '3']):
            app.move_doc_to_shelf()
        self.assertGreater(len(self.dirs['3']), before_to)
        self.assertLess(len(self.dirs['2']), before_from)