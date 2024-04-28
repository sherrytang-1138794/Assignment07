from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime, datetime

from barkyapi.models import Bookmark
from barkyarch.domain.model import DomainBookmark
from barkyarch.services.commands import (
    AddBookmarkCommand,
    ListBookmarksCommand,
    DeleteBookmarkCommand,
    EditBookmarkCommand,
)


class TestCommands(TestCase):
    def setUp(self):
        right_now = localtime().date()
    
        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Test Bookmark",
            url="http://www.example.com",
            notes="Test notes",
            date_added=right_now,
        )

        self.domain_bookmark_2 = DomainBookmark(
            id=2,
            title="Test Bookmark 2",
            url="http://www.example2.com",
            notes="Test notes 2",
            date_added=right_now,
        )

    def test_command_add(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # run checks
        # print("*"*20, "add testing")
        # print(f"bookmark: {Bookmark.objects.all()}")

        # one object is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we inserted
        self.assertEqual(Bookmark.objects.get(id=1).url, self.domain_bookmark_1.url)

    
    def test_command_list(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)
        add_command.execute(self.domain_bookmark_2)
        
        list_command = ListBookmarksCommand()
        list_command.execute(Bookmark)
        # print("*"*20, "list testing")

        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.first().date_added, self.domain_bookmark_1.date_added) #Cause AddBookmarkCommand.execute() has setted bookmark.timestamp, bookmark1 will always created before bookmark2



    def test_command_edit(self):
        right_now = localtime().date()
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # print("*"*20, "edit testing")
        # print(f"original bookmark: {self.domain_bookmark_1}")
       
        self.domain_bookmark_1 = DomainBookmark(
            id=1,
            title="Updated Test Bookmark",
            url="http://www.example.com",
            notes="Test notes Updated",
            date_added=right_now,
        )
        
        # print(f"updated bookmark: {self.domain_bookmark_1}")
        EditBookmarkCommand.execute(self, data=self.domain_bookmark_1)
        
        # one object is inserted
        self.assertEqual(Bookmark.objects.count(), 1)

        # that object is the same as the one we updated
        self.assertEqual(Bookmark.objects.get(id=1).title, self.domain_bookmark_1.title)
        



    def test_command_delete(self):
        add_command = AddBookmarkCommand()
        add_command.execute(self.domain_bookmark_1)

        # print("*"*20, "delete testing")
        # print(f"original bookmark: {Bookmark.objects.all()}")

        delete_command = DeleteBookmarkCommand()
        delete_command.execute(self.domain_bookmark_1)

        # print(f"updated bookmark: {Bookmark.objects.all()}")

        self.assertEqual(Bookmark.objects.count(), 0)



        
