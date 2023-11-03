from unittest import TestCase
from modules.plagiarism import Plagiarism


class TestPlagiarism(TestCase):
    def test_do_hash(self):
        plagiarism = Plagiarism('./hash', ['Instructions.txt'])
        results = plagiarism.check_hash()

        self.assertEqual(7, len(results))

        # Check "f1", a double file instance of plagiarism
        self.assertIn((('hash\\Alan Cox f1\\main.py',
                        '4e993d638d9ecaba22f445033b81736e0bcb1da1d1d145fc17e1ce14363b75be',
                        'Alan Cox f1'),
                       ('hash\\John Piper f1\\main.py',
                        '4e993d638d9ecaba22f445033b81736e0bcb1da1d1d145fc17e1ce14363b75be',
                        'John Piper f1')),
                      results)
        self.assertIn((('hash\\Alan Cox f1\\Nested Folder\\Something.txt',
                        '8b888bc209da2a6874e7d5124b76dcd9d95c401cb5f1b45f1c70ba034d8322e7',
                        'Alan Cox f1'),
                       ('hash\\John Piper f1\\Nested Folder\\Something.txt',
                        '8b888bc209da2a6874e7d5124b76dcd9d95c401cb5f1b45f1c70ba034d8322e7',
                        'John Piper f1')),
                      results)

        # Check "f2", an instance of one file being plagiarized among three submissions
        self.assertIn((('hash\\Bill Gates f2\\File1.txt',
                        'ea727f81ee1e262973d68528acfdd3dcc52cc5aea1c7a2f4023689e61ed06a7f',
                        'Bill Gates f2'),
                       ('hash\\Dave Plummer f2\\File1.txt',
                        'ea727f81ee1e262973d68528acfdd3dcc52cc5aea1c7a2f4023689e61ed06a7f',
                        'Dave Plummer f2')),
                      results)
        self.assertIn((('hash\\Bill Gates f2\\File1.txt',
                        'ea727f81ee1e262973d68528acfdd3dcc52cc5aea1c7a2f4023689e61ed06a7f',
                        'Bill Gates f2'),
                       ('hash\\Steve Jobs f2\\File1.txt',
                        'ea727f81ee1e262973d68528acfdd3dcc52cc5aea1c7a2f4023689e61ed06a7f',
                        'Steve Jobs f2')),
                      results)

        # Check "f3", plagiarism with just a file name change
        self.assertIn((('hash\\Jens Axboe f3\\Cats.txt',
                        'bcc33f0b81d2d3129deb62ac658cd0ac9362040a58cee75fc3067e180f95bbef',
                        'Jens Axboe f3'),
                       ('hash\\Moshe Bar f3\\not_Cats.txt',
                        'bcc33f0b81d2d3129deb62ac658cd0ac9362040a58cee75fc3067e180f95bbef',
                        'Moshe Bar f3')),
                      results)

        # Check "f4", an instance of a single file being copied
        self.assertIn((('hash\\Aunt Suzie f4\\Submission.txt',
                        'f28bdc51f61d96e85d1a293616576e89fcb794c810192a4a01dfd7454b6e6c48',
                        'Aunt Suzie f4'),
                       ('hash\\Steve Wozniak f4\\Submission.txt',
                        'f28bdc51f61d96e85d1a293616576e89fcb794c810192a4a01dfd7454b6e6c48',
                        'Steve Wozniak f4')),
                      results)

        # Check "f5", an instance of a single file being copied but in a folder
        self.assertIn((('hash\\Pope Anacletusn f5\\Some folder\\Lorem.txt',
                        '2d8c2f6d978ca21712b5f6de36c9d31fa8e96a4fa5d8ff8b0188dfb9e7c171bb',
                        'Pope Anacletusn f5'),
                       ('hash\\Pope Linus f5\\Lorem.txt',
                        '2d8c2f6d978ca21712b5f6de36c9d31fa8e96a4fa5d8ff8b0188dfb9e7c171bb',
                        'Pope Linus f5')),
                      results)
