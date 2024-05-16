from hazm import Normalizer

from task_extractor.extractor import TaskExtractor


def main():
    normalizer = Normalizer()
    while True:
        try:
            sent = str(input('دستور را وارد کن و برای خروج بنویس خروج:\n'))
            if sent == 'خروج':
                break
            # sent = 'یادم‌ باشه هر روز ساعت 12 ظهر به یادگیری برنامه‌نویسی بپردازم.'
            # sent = 'یادگیری برنامه‌نویسی روزانه‌ام را لغو کن.'
            # sent = 'کار تماس با دوستم انجام شد.'
            # sent = 'زمان تماس با دوستم در 12 فروردین را به 9:30 شب تغییر بده.'
            # sent = 'برنامه هفتگی‌ام را نشان بده.'
            sent = normalizer.normalize(sent)
            extractor = TaskExtractor()
            res = extractor.run(sent)
            print(res)
        except Exception as e:
            print(e)
            continue


# print("Gregorian Date:", JalaliDate(year=1403, month=2, day=26).to_gregorian())
# print("Jalali Date:", JalaliDate(datetime.now()))

# https://pypi.org/project/persiantools/#:~:text=Provides%20Jalali%20(also%20known%20as,%2C%20%3D%3D%20%2C%20and%20%3E%3D%20.
# برای نصب تاریخ

if __name__ == '__main__':
    main()
