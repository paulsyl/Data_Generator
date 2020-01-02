from faker.providers import BaseProvider
import sys
from datetime import datetime
import time


class HMRCProvider(BaseProvider):
    """ A HMRC Specific Data Provider
    """
    class Meta:
        name = "HMRC Specific Data Provider"

    def __init__(self, *args, **kwargs):

        self.postcodes = [line.rstrip('\n') for line in open('data_providers/postcodes.txt')]
        # Initalisation of Dimension Key when Class in instantiated.
        self.uniq = 1

        super().__init__(*args, **kwargs)

    def nino(self) -> str:
        invalidNino = ['BG','GB','NK','KN','TN','NT','ZZ']
        prefix = 'BG'
        if prefix in invalidNino:
            prefix = self.random_element("ABCEGHJKLMNOPRSTUWXYZ") + self.random_element("ABCEGHJKLMNPRSTUWXYZ")

        digit = '{:0>6}'.format(self.random_int(0,999999))
        suffix = self.random_element('ABCD')

        return prefix + digit + suffix

    def uk_postcode(self) -> str:

        return self.random_element(self.postcodes)

    def unique_key(self):
        curr_key = self.uniq
        self.uniq = self.uniq + 1
        return curr_key

    def dim_from_list(self, list_of_elements:list, parent_instance:int):
        # Validate the configuration to ensure only unique values returned
        if len(list_of_elements) < parent_instance:
            msg = 'ERROR:  {} : Attempting to generate more dimension records than keys presented - {} \
            \n* Please check configuration file *'.format(parent_instance, len(list_of_elements))
            sys.exit(msg)

        # List indexes start at 0
        key = parent_instance - 1
        return list_of_elements[key]

    def reference_table(self, reference_values:list, index:int):
        # Create data based up on a list of Values supplied into the function call.
        if len(reference_values) < index + 1:
            msg = 'ERROR:  {} : Attempting to generate more dimension records than keys presented - {} \
            \n* Please check configuration file *'.format(index, len(reference_values))
            sys.exit(msg)

        # List indexes start at 0
        key = index - 1
        return reference_values[key]

    def uk_vat_reg_no(self) -> str:
        digits_3 = self.random_number(digits=3, fix_len=True)
        digits_4 = self.random_number(digits=4, fix_len=True)
        digits_2 = self.random_number(digits=2, fix_len=True)

        return 'GB' + str(digits_3) + str(digits_4) + str(digits_2)

    def empty_string(self):
        return ''

    def gb_passport(self) -> str:
        digits_10 = self.random_number(digits=10, fix_len=True)
        country_code = "".join(self.random_letters(length=3)).upper()
        digits_7 = self.random_number(digits=7, fix_len=True)
        code = self.random_element(elements=('U','M','F'))
        digits_9 = self.random_number(digits=9, fix_len=True)
        return str(digits_10) + country_code + str(digits_7) + code + str(digits_9)

    def date_between_two_string_dates(self, start_date:str ='19700101',end_date:str ='now', dt_format:str = '%Y%m%d'):
        """
        Custom Provider:
        Get a DateTime object based on a random date between two given dates provided as strings.
        Accepts date /datetime strings in any provided format, default is YYYYMMDD.
        :param start_date Defaults to 1st Jan 1980
        :param end_date Defaults to "now"
        :return Date
        """
        if end_date == 'now':
            unix_end_date = time.mktime(datetime.now().timetuple())
        else:
            unix_end_date = time.mktime(datetime.strptime(end_date, dt_format).timetuple())

        unix_start_date = time.mktime(datetime.strptime(start_date, dt_format).timetuple())

        return datetime.utcfromtimestamp(self.generator.random_int(min=unix_start_date,max=unix_end_date)).strftime(dt_format)
