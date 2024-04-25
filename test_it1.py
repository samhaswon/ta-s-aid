import unittest
from Event import Event
from Contact import Contact


class TestThings(unittest.TestCase):
    def setUp(self) -> None:
        """
        Set up some commonly used object among test functions.
        :return: None
        """
        self.contact_dict_1: dict = {
            "FirstName": "Amani",
            "LastName": "Altarawneh",
            "UID": 0,
            "EmailAddress": "aaltarawneh@tntech.edu",
            "Dept": "Computer Science",
            "Title": "Assistant Professor",
            "Phone": "--",
            "Building": "Bruner Hall (BRUN) 232",
            "POBox": "5101"
        }
        self.contact_dict_2: dict = {
            "FirstName": "John",
            "LastName": "Doe",
            "UID": 1,
            "EmailAddress": "jdoe@example.com",
            "Dept": "Engineering",
            "Title": "Engineer",
            "Phone": "123-456-7890",
            "Building": "Smith Hall (SMTH) 101",
            "POBox": "12345"
        }
        self.contact_dict_3: dict = {
            "FirstName": "Emily",
            "LastName": "Smith",
            "UID": 2,
            "EmailAddress": "emilysmith@example.com",
            "Dept": "Computer Science",
            "Title": "Associate Professor",
            "Phone": "555-555-5555",
            "Building": "Bruner Hall",
            "POBox": "6789"
        }
        self.event_1: dict = {
            "Name": "Lecture on AI",
            "UID": 0,
            "Date": "2023-10-15",
            "StartTime": "14:00",
            "Location": "Bruner 228",
            "Duration": 2
        }
        self.event_2: dict = {
            "Name": "Music Concert",
            "UID": 2,
            "Date": "2023-12-08",
            "StartTime": "19:30",
            "Location": "University Auditorium",
            "Duration": 2
        }

    def test_contact_creation(self):
        """
        Test the creation and proper attribute assignment of the Contact class
        :return:
        """
        # From contacts.json
        self.contact_1 = Contact(self.contact_dict_1)
        try:
            self.assertEqual(self.contact_1.firstname, "Amani")
        except AttributeError:
            self.assertEqual(self.contact_1.first_name, "Amani")
        try:
            self.assertEqual(self.contact_1.lastname, "Altarawneh")
        except AttributeError:
            self.assertEqual(self.contact_1.last_name, "Altarawneh")
        try:
            self.assertIn(self.contact_1.uid, [0, "0"])
        except AttributeError:
            self.assertIn(self.contact_1.UID, [0, "0"])
        self.assertEqual(self.contact_1.email, "aaltarawneh@tntech.edu")
        try:
            self.assertEqual(self.contact_1.department, "Computer Science")
        except AttributeError:
            self.assertEqual(self.contact_1.dept, "Computer Science")
        self.assertEqual(self.contact_1.title, "Assistant Professor")
        try:
            self.assertEqual(self.contact_1.phone, "--")
        except AttributeError:
            self.assertEqual(self.contact_1.phone_number, "--")
        self.assertEqual(self.contact_1.building, "Bruner Hall (BRUN) 232")
        try:
            self.assertEqual(self.contact_1.mail_code, "5101")
        except AttributeError:
            self.assertEqual(self.contact_1.pobox, "5101")
        try:
            self.assertIn(self.contact_1.last_contact, ["", None, 'None', 'undefined', 'N/A'])
        except AttributeError:
            self.assertIn(self.contact_1.lastcontact, ["", None, 'None', 'undefined', 'N/A'])

        # Just some random data to test with
        self.contact_2 = Contact(self.contact_dict_2)
        try:
            self.assertEqual(self.contact_2.firstname, "John")
        except AttributeError:
            self.assertEqual(self.contact_2.first_name, "John")
        try:
            self.assertEqual(self.contact_2.lastname, "Doe")
        except AttributeError:
            self.assertEqual(self.contact_2.last_name, "Doe")
        try:
            self.assertIn(self.contact_2.uid, [1, "1"])
        except AttributeError:
            self.assertIn(self.contact_2.UID, [1, "1"])
        self.assertEqual(self.contact_2.email, "jdoe@example.com")
        try:
            self.assertEqual(self.contact_2.department, "Engineering")
        except AttributeError:
            self.assertEqual(self.contact_2.dept, "Engineering")
        self.assertEqual(self.contact_2.title, "Engineer")
        try:
            self.assertEqual(self.contact_2.phone, "123-456-7890")
        except AttributeError:
            self.assertEqual(self.contact_2.phone_number, "123-456-7890")
        self.assertEqual(self.contact_2.building, "Smith Hall (SMTH) 101")
        try:
            self.assertEqual(self.contact_2.mail_code, "12345")
        except AttributeError:
            self.assertEqual(self.contact_2.pobox, "12345")
        try:
            self.assertIn(self.contact_2.last_contact, ["", None, 'None', 'undefined', 'N/A'])
        except AttributeError:
            self.assertIn(self.contact_2.last_contact, ["", None, 'None', 'undefined', 'N/A'])

    def test_last_contact(self):
        """
        Test the last contact attribute of the Contact class
        :return: None
        """
        self.contact_1 = Contact(self.contact_dict_1)
        try:
            self.assertIn(self.contact_1.last_contact, ["", None, 'None', 'undefined', 'N/A'])
            self.contact_1.last_contact = "1970-1-1"  # the Unix epoch 😎
            self.assertEqual(self.contact_1.last_contact, "1970-1-1")
        except AttributeError:
            self.assertIn(self.contact_1.lastcontact, ["", None, 'None', 'undefined', 'N/A'])
            self.contact_1.lastcontact = "1970-1-1"  # the Unix epoch 😎
            self.assertEqual(self.contact_1.lastcontact, "1970-1-1")

    def test_contact_str(self):
        """
        Test the string method of the Contact class
        :return: None
        """
        self.contact_1 = Contact(self.contact_dict_1)
        self.contact_2 = Contact(self.contact_dict_2)
        self.contact_3 = Contact(self.contact_dict_3)

        self.assertEqual(self.contact_1.__str__(),
                         "Amani Altarawneh\n"
                         "Title: Assistant Professor\n"
                         "Email: aaltarawneh@tntech.edu\n"
                         "Department: Computer Science\n"
                         "Phone: --\n"
                         "Building: Bruner Hall (BRUN) 232\nLDC: ")

        self.assertEqual(self.contact_2.__str__(),
                         "John Doe\n"
                         "Title: Engineer\n"
                         "Email: jdoe@example.com\n"
                         "Department: Engineering\n"
                         "Phone: 123-456-7890\n"
                         "Building: Smith Hall (SMTH) 101\nLDC: ")

        self.assertEqual(self.contact_3.__str__(),
                         "Emily Smith\n"
                         "Title: Associate Professor\n"
                         "Email: emilysmith@example.com\n"
                         "Department: Computer Science\n"
                         "Phone: 555-555-5555\n"
                         "Building: Bruner Hall\nLDC: ")

    def test_contact_getters(self):
        """
        Test that attributes of the contact class are not implemented in a more C++ style of OOP.
        This function tests for the usage of the property decorator.
        :return: None
        """
        self.contact = Contact(self.contact_dict_1)

        try:
            self.assertFalse(callable(getattr(self.contact, "lastname")),
                             msg="lastname should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(self.contact, "last_name")),
                             msg="lastname should only be a property using the property decorator")
        try:
            self.assertFalse(callable(getattr(self.contact, "firstname")),
                             msg="firstname should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(self.contact, "first_name")),
                             msg="firstname should only be a property using the property decorator")
        try:
            self.assertFalse(callable(getattr(self.contact, "uid")),
                             msg="uid should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(self.contact, "UID")),
                             msg="uid should only be a property using the property decorator")
        self.assertFalse(callable(getattr(self.contact, "email")),
                         msg="email should only be a property using the property decorator")
        try:
            self.assertFalse(callable(getattr(self.contact, "department")),
                             msg="department should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(self.contact, "dept")),
                             msg="department should only be a property using the property decorator")
        self.assertFalse(callable(getattr(self.contact, "title")),
                         msg="title should only be a property using the property decorator")
        self.assertFalse(callable(getattr(self.contact, "phone")),
                         msg="phone should only be a property using the property decorator")
        self.assertFalse(callable(getattr(self.contact, "building")),
                         msg="building should only be a property using the property decorator")
        try:
            self.assertFalse(callable(getattr(self.contact, "mail_code")),
                             msg="mail_code should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(self.contact, "pobox")),
                             msg="mail_code should only be a property using the property decorator")
        # last_contact is covered in test_last_contact()

    def test_event_creation(self):
        """
        Test the creation and proper assignment of attributes to the Event class
        :return: None
        """
        event_1 = Event(self.event_1)
        self.assertEqual(event_1.name, "Lecture on AI")
        try:
            self.assertEqual(event_1.uid, 0)
        except AttributeError:
            self.assertEqual(event_1.UID, 0)
        self.assertEqual(event_1.date, "2023-10-15")
        self.assertEqual(event_1.start_time, "14:00")
        self.assertEqual(event_1.location, "Bruner 228")
        self.assertEqual(event_1.duration, 2)

        event_2 = Event(self.event_2)
        self.assertEqual(event_2.name, "Music Concert")
        try:
            self.assertEqual(event_2.uid, 2)
        except AttributeError:
            self.assertEqual(event_2.UID, 2)
        self.assertEqual(event_2.date, "2023-12-08")
        self.assertEqual(event_2.start_time, "19:30")
        self.assertEqual(event_2.location, "University Auditorium")
        self.assertEqual(event_2.duration, 2)

    def test_event_str(self):
        """
        Test the string method of the Event class
        :return: None
        """
        event_1 = Event(self.event_1)
        expected_str_1 = "Event: Lecture on AI\nDate: 2023-10-15\nStart time: 14:00\nDuration: 2 hours\nLocation: " \
                         "Bruner 228"
        self.assertEqual(str(event_1), expected_str_1)

        event_2 = Event(self.event_2)
        expected_str_2 = "Event: Music Concert\nDate: 2023-12-08\nStart time: 19:30\nDuration: 2 hours\nLocation: " \
                         "University Auditorium"
        self.assertEqual(str(event_2), expected_str_2)

    def test_event_getters(self):
        event = Event(self.event_1)

        self.assertFalse(callable(getattr(event, "name")),
                         msg="name should only be a property using the property decorator")
        try:
            self.assertFalse(callable(getattr(event, "uid")),
                             msg="uid should only be a property using the property decorator")
        except AttributeError:
            self.assertFalse(callable(getattr(event, "UID")),
                             msg="uid should only be a property using the property decorator")
        self.assertFalse(callable(getattr(event, "date")),
                         msg="date should only be a property using the property decorator")
        self.assertFalse(callable(getattr(event, "start_time")),
                         msg="start_time should only be a property using the property decorator")
        self.assertFalse(callable(getattr(event, "location")),
                         msg="location should only be a property using the property decorator")
        self.assertFalse(callable(getattr(event, "duration")),
                         msg="duration should only be a property using the property decorator")


if __name__ == '__main__':
    unittest.main()
