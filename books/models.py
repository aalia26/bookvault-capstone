from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Represents a book available in the online bookstore.

    Fields:
        title (CharField): The title of the book.
        author (CharField): The author's name.
        description (TextField): A detailed summary of the book.
        price (DecimalField): The retail price of the book.
        cover_image (ImageField): Optional image of the book's cover.
        release_date (DateField): Optional release date of the book.
        is_popular (BooleanField): Flag to mark book as popular.
        is_upcoming (BooleanField): Flag to indicate if the book is unreleased.

    Returns:
        str: Title of the book.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    release_date = models.DateField(null=True, blank=True)
    is_popular = models.BooleanField(default=False)
    is_upcoming = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Stores a review submitted by a user for a specific book.

    Fields:
        book (ForeignKey): Reference to the reviewed book.
        user (ForeignKey): The user who submitted the review.
        content (TextField): The body of the review.
        created_at (DateTimeField): Timestamp when the review was created.

    Returns:
        str: Username and book title of the review.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.book.title}'


class Cart(models.Model):
    """
    Represents a shopping cart linked to a single user.

    Fields:
        user (OneToOneField): The user who owns the cart.
        created_at (DateTimeField): Timestamp when the cart was created.

    Properties:
        total_price (Decimal): The total cost of all items in the cart.

    Returns:
        str: A string indicating the cart owner.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'

    @property
    def total_price(self):
        """
        Calculate the total cost of all items in the cart.

        Returns:
            Decimal: Sum of all cart item prices.
        """
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """
    Represents a single book and its quantity in a user's cart.

    Fields:
        cart (ForeignKey): Reference to the user's cart.
        book (ForeignKey): The book being added to the cart.
        quantity (PositiveIntegerField): The number of copies.

    Properties:
        total_price (Decimal): Total price for this line item (price * quantity).
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        """
        Calculate the total cost for this item based on quantity.

        Returns:
            Decimal: Total price for the book(s) in this item.
        """
        return self.book.price * self.quantity


class UpcomingBook(models.Model):
    """
    Represents a book that is planned for future release.

    Fields:
        title (CharField): The title of the upcoming book.
        author (CharField): The author’s name.
        release_date (DateField): The expected release date.
        cover_image (ImageField): Optional cover image of the upcoming book.
        description (TextField): Optional short summary.

    Returns:
        str: Title of the upcoming book.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='upcoming_book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
