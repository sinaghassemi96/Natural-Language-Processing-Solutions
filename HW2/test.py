import unittest
from task_extractor.extractor import TaskExtractor

class TestTaskExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = TaskExtractor()

    def test_default(self):
        sent = 'باید تسک حل تمرین دوم درس را در یک آذر شروع کنیم و تا ده آذر تمام کنیم.'
        self.extractor.run(sent)
        self.assertEqual(len(self.extractor.tasks), 1)
        self.assertEqual(self.extractor.tasks[0].name, 'حل تمرین دوم درس')
        self.assertEqual(self.extractor.tasks[0].start_date, 'یک آذر')
        self.assertEqual(self.extractor.tasks[0].end_date, 'ده آذر')
        self.assertFalse(self.extractor.tasks[0].is_done)
        self.assertEqual(self.extractor.tasks[0].assignees, [])
        self.assertEqual(self.extractor.tasks[0].subtasks, [])
        sent = 'برای اینکار باید اول موضوع را مشخص کنیم و بعد پیاده‌سازی را انجام دهیم.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].subtasks, ['موضوع را مشخص کنیم', 'پیاده‌سازی را انجام دهیم'])
        sent = 'افراد مسئول حل این تمرین آرش و ریحانه هستن.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].assignees, ['آرش', 'ریحانه'])
        sent = 'ددلاین تسک به 15 آذر منتقل شد.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].end_date, '۱۵ آذر')
        sent = 'تسک حل تمرین دوم درس تمام شد.'
        self.extractor.run(sent)
        self.assertTrue(self.extractor.tasks[0].is_done)
        self.assertEqual(len(self.extractor.tasks), 1)
        print(self.extractor.tasks)

    def test_declare_end_only(self):
        sent = 'تسک ارائه مقاله باید تا بیستم بهمن تمام شود.'
        self.extractor.run(sent)
        self.assertEqual(len(self.extractor.tasks), 1)
        self.assertEqual(self.extractor.tasks[0].name, 'ارائه مقاله')
        self.assertEqual(self.extractor.tasks[0].start_date, '')
        self.assertEqual(self.extractor.tasks[0].end_date, 'بیستم بهمن')
        self.assertFalse(self.extractor.tasks[0].is_done)
        self.assertEqual(self.extractor.tasks[0].assignees, [])
        self.assertEqual(self.extractor.tasks[0].subtasks, [])
        sent = 'برای اتمام به موقع آن، باید ۱ بهمن آن تسک را شروع کنیم.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].start_date, '۱ بهمن')
        sent = 'این تسک شامل پیدا کردن مقاله مناسب و سپس یادداشت برداری از آن است.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].subtasks, ['پیدا کردن مقاله مناسب', 'یادداشت‌برداری از آن'])
        sent = 'مسئولین انجام این تسک، حسین و علی می‌باشند.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].assignees, ['حسین', 'علی'])
        self.assertEqual(len(self.extractor.tasks), 1)

    def test_declare_assignment_end(self):
        sent = 'مسئولیت تسک حل تمرین سوم درس با مهران و علی است.'
        self.extractor.run(sent)
        self.assertEqual(len(self.extractor.tasks), 1)
        self.assertEqual(self.extractor.tasks[0].name, 'حل تمرین سوم درس')
        self.assertEqual(self.extractor.tasks[0].start_date, '')
        self.assertEqual(self.extractor.tasks[0].end_date, '')
        self.assertFalse(self.extractor.tasks[0].is_done)
        self.assertEqual(self.extractor.tasks[0].assignees, ['مهران', 'علی'])
        self.assertEqual(self.extractor.tasks[0].subtasks, [])
        sent = 'ددلاین این تسک ۱۵ دی می‌باشد.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].end_date, '۱۵ دی')
        sent = 'این تسک از ۲۷ آذر شروع می‌شود.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].start_date, '۲۷ آذر')
        sent = 'برای این تسک باید ابتدا دیتاست مناسب پیدا کنیم و سپس مدل گفته شده را روی آن آموزش دهیم.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].subtasks, ['دیتاست مناسب پیدا کنیم', 'مدل گفته‌شده را روی آن آموزش دهیم'])
        sent = 'زمان تحویل این تسک تا 25 دی تمدید شد.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].end_date, '۲۵ دی')
        self.assertEqual(len(self.extractor.tasks), 1)

    def test_declare_assignment_first(self):
        sent = 'امیر و علیرضا مسئول تسک آماده‌سازی داده‌های تمرین هستند.'
        self.extractor.run(sent)
        self.assertEqual(len(self.extractor.tasks), 1)
        self.assertEqual(self.extractor.tasks[0].name, 'آماده‌سازی داده‌های تمرین')
        self.assertEqual(self.extractor.tasks[0].start_date, '')
        self.assertEqual(self.extractor.tasks[0].end_date, '')
        self.assertFalse(self.extractor.tasks[0].is_done)
        self.assertEqual(self.extractor.tasks[0].assignees, ['امیر', 'علیرضا'])
        self.assertEqual(self.extractor.tasks[0].subtasks, [])
        sent = 'آنها انجام تسک را از بیست و یکم فروردین شروع می‌کنند.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].start_date, 'بیست و یکم فروردین')
        sent = 'برای این وظیفه باید ابتدا داده‌ها را تمیز کرده و سپس پیش‌پردازش کنند.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].subtasks, ['داده‌ها را تمیز کرده', 'پیش‌پردازش کنند'])
        sent = 'مهلت تحویل این تسک تا ۱ اردیبهشت می‌باشد.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].end_date, '۱ اردیبهشت')
        sent = 'این تسک انجام شد.'
        self.extractor.run(sent)
        self.assertTrue(self.extractor.tasks[0].is_done)
        self.assertEqual(len(self.extractor.tasks), 1)

    def test_subtask_multiple(self):
        sent = 'مسئولین وظیفه بررسی متون قدیمی با مهران و علی و سارا است.'
        self.extractor.run(sent)
        self.assertEqual(len(self.extractor.tasks), 1)
        self.assertEqual(self.extractor.tasks[0].name, 'بررسی متون قدیمی')
        self.assertEqual(self.extractor.tasks[0].start_date, '')
        self.assertEqual(self.extractor.tasks[0].end_date, '')
        self.assertFalse(self.extractor.tasks[0].is_done)
        self.assertEqual(self.extractor.tasks[0].assignees, ['مهران', 'علی', 'سارا'])
        self.assertEqual(self.extractor.tasks[0].subtasks, [])
        sent = 'برای اینکار باید اول متون را پیدا کنیم و سپس آن‌ها را دسته‌بندی کنیم و بعد آن‌ها رو تحلیل کنیم.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].subtasks, ['متون را پیدا کنیم', 'آن‌ها را دسته‌بندی کنیم', 'آن‌ها رو تحلیل کنیم'])
        sent = 'این تسک از ۲۷ خرداد شروع می‌شود.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].start_date, '۲۷ خرداد')
        sent = 'مهلت تحویل این تسک تا یازدهم شهریور می‌باشد.'
        self.extractor.run(sent)
        self.assertEqual(self.extractor.tasks[0].end_date, 'یازدهم شهریور')
        sent = 'این تسک پایان یافت.'
        self.extractor.run(sent)
        self.assertTrue(self.extractor.tasks[0].is_done)
        self.assertEqual(len(self.extractor.tasks), 1)

if __name__ == '__main__':
    unittest.main()