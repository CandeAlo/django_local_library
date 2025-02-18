from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from uuid import uuid4
from django.conf import settings
from datetime import date

class Genre(models.Model):
    """
    Represents a literacy genre (e.g. Poetry, Fantasy, Cuisine...).
    """
    name = models.CharField(
        max_length=200,
        help_text="Name of the genre")

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Genre already exists" 
                                        "(case insensitive match)"
            ),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the absolute URL of a particular genre.
        """
        return reverse('genre-detail', args=[str(self.id)])


class Language(models.Model):
    """
    Represents a language (e.g. English, Spanish, Huttese...).
    """
    name = models.CharField(
        max_length=200,
        help_text="Name of the language")

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Language already exists" 
                                        "(case insensitive match)"
            ),
        ]

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        """
        Returns the absolute URL of a particular language.
        """
        return reverse('language-detail', args=[str(self.id)])


class Author(models.Model):
    """
    Represents an author.
    """
    first_name = models.CharField(
        max_length=100,
        help_text="First name of the author")

    last_name = models.CharField(
        max_length=100,
        help_text="Last name of the author")

    date_of_birth = models.DateField(
        verbose_name='birth',
        null=True,
        blank=True,
        help_text="Date of birth of the author")

    date_of_death = models.DateField(
        verbose_name='Died',
        null=True,
        blank=True,
        help_text="Date of death of the author")

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_absolute_url(self):
        """
        Returns the absolute URL of an author.
        """
        return reverse("author-detail", args=str(self.id))


class Book(models.Model):
    """
    Represents a book.
    """
    title = models.CharField(
        max_length=200,
        help_text="Enter title of the book")
        
    # Foreign Key used because book can only have one author, 
    # but authors can have multiple books.
    # Author as a string rather than object because it hasn't 
    # been declared yet in file.

    author = models.ForeignKey(
        to='Author',
        on_delete=models.RESTRICT,
        null=True,
        help_text="Enter author of the book")

    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the book")

    isbn = models.CharField(
        verbose_name='ISBN',
        max_length=13,
        unique=True,
        help_text='"13 Caracteres " \
            "<a href=https://www.isbn-international.org/content/what-isbn" \
            ">ISBN number</a>"')

    # ManyToManyField used because genre can contain many books.
    # Books can cover many genres.
    # Genre class has already been defined so we can specify the object 
    # above.

    genre = models.ManyToManyField(
        to=Genre,
        help_text="Select a genre for this book")

    language = models.ForeignKey(
        to=Language,
        on_delete=models.RESTRICT,
        null=True,
        help_text="Select a language for this book")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def display_genre(self):
        """
        Creates a string with the first three genres. It is required for
        displaying the book in the admin page.
        """
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Returns the absolute URL of a book.
        """
        return reverse("book-detail", args=str(self.id))


class BookInstance(models.Model):
    """
    Represents a specific copy of a book (i.e. that can be borrowed
    from the library).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        help_text="Unique identifier of the book copy")

    book = models.ForeignKey(
        to=Book,
        on_delete=models.RESTRICT,
        null=True,
        help_text="Book")

    imprint = models.CharField(
        max_length=200,
        help_text="Imprint of the book")

    due_back = models.DateField(
        null=True,
        blank=True,
        help_text="Due date to return the book")

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text="Availability of the book")
 
    borrower = models.ForeignKey(
    	settings.AUTH_USER_MODEL,
    	on_delete=models.SET_NULL,
    	null=True,
    	blank=True,
    )

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        """
        Determines if the book is overdue based on due date and current date.
        """
        return bool(self.due_back and date.today() > self.due_back)
