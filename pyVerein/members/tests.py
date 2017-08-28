# Import TestCase.
from django.test import TestCase
# Import Membermodel.
from .models import Member
# Import datetime
from datetime import datetime, timedelta

class MemberTestMethods(TestCase):
    # Test for get_full_name method.
    def test_get_full_name(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # Assert if full name is "first last".
        self.assertEqual(member.get_full_name(), 'first last')

    # Test for is_terminated method.
    def test_is_terminated(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # New member should not be terminated
        self.assertFalse(member.is_terminated())

        # Set terminated date to future value
        member.terminated_at = datetime.now().date() + timedelta(days=1)

        # Member with terminated_at date in the future should not be terminated
        self.assertFalse(member.is_terminated())

        # Set terminated date to today value
        member.terminated_at = datetime.now().date()

        # Member with terminated_at date today should be terminated
        self.assertTrue(member.is_terminated())

        # Set terminated date to past value
        member.terminated_at = datetime.now().date() - timedelta(days=1)

        # Member with terminated_at date in the past should be terminated
        self.assertTrue(member.is_terminated())

    # Test for __str__ method.
    def test__str__(self):
        # Create Member.
        member = Member.objects.create(first_name="first", last_name="last")

        # Assert if __str__ ist full name.
        self.assertEqual(str(member), "first last")
