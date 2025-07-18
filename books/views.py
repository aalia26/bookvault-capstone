from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from .forms import UpcomingBookForm
from .models import Book, Review, Cart, CartItem, UpcomingBook


def home(request):
    """
    Render the homepage with key dynamic content.

    Retrieves and displays:
    - The 5 nearest upcoming book releases.
    - The 5 most popular books (where is_popular=True).
    - The 5 most recent reviews with related book and user data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered homepage with context data.
    """
    upcoming_books = UpcomingBook.objects.all().order_by('release_date')[:5]
    popular_books = Book.objects.filter(is_popular=True)[:5]
    recent_reviews = Review.objects.select_related('book', 'user').order_by('-created_at')[:5]

    context = {
        'upcoming_books': upcoming_books,
        'popular_books': popular_books,
        'recent_reviews': recent_reviews,
    }
    return render(request, 'books/home.html', context)


def book_list(request):
    """
    Display a list of books with optional search filtering.

    If a query parameter (`q`) is provided, filters books by title or author.
    Otherwise, displays all books.

    Args:
        request (HttpRequest): The HTTP request containing optional 'q' parameter.

    Returns:
        HttpResponse: Rendered book list view with search results or full list.
    """
    query = request.GET.get('q')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query)) if query else Book.objects.all()
    context = {'books': books, 'query': query}
    return render(request, 'books/book_list.html', context)


def book_detail(request, pk):
    """
    Display details and reviews of a specific book.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the book.

    Returns:
        HttpResponse: Rendered detail page for the selected book.
    """
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().order_by('-created_at')
    context = {'book': book, 'reviews': reviews}
    return render(request, 'books/book_detail.html', context)


@login_required
def add_review(request, pk):
    """
    Allow a logged-in user to submit a review for a specific book.

    Args:
        request (HttpRequest): The HTTP request object (must be POST to submit).
        pk (int): Primary key of the book being reviewed.

    Returns:
        HttpResponse: Redirects to book detail page on success, or shows review form.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Review.objects.create(book=book, user=request.user, content=content)
            return redirect('book_detail', pk=book.pk)
    return render(request, 'books/add_review.html', {'book': book})


def signup(request):
    """
    Handle new user registration.

    On successful submission, logs in the user and redirects to the homepage.

    Args:
        request (HttpRequest): The HTTP request with optional POST data.

    Returns:
        HttpResponse: Renders registration form or redirects on successful sign-up.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
@login_required
def add_to_cart(request, book_id):
    """
    Add a book to the logged-in user's cart.

    If the book is already in the cart, increments its quantity.

    Args:
        request (HttpRequest): The HTTP request.
        book_id (int): ID of the book to add to the cart.

    Returns:
        HttpResponse: Redirect to cart detail page.
    """
    book = get_object_or_404(Book, pk=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    """
    Display the current user's cart contents.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered cart detail page with cart items.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'books/cart_detail.html', {'cart': cart})


@login_required
def remove_from_cart(request, item_id):
    """
    Remove a specific item from the user's cart.

    Args:
        request (HttpRequest): The HTTP request.
        item_id (int): The CartItem ID to remove.

    Returns:
        HttpResponse: Redirect to the cart detail page.
    """
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')


@login_required
def upload_upcoming_book(request):
    """
    Allow staff users to upload an upcoming book (title, cover, date, etc.).

    Accepts both GET and POST. Requires user to be logged in.
    Files (like book covers) must be handled via `request.FILES`.

    Args:
        request (HttpRequest): The HTTP request, possibly with form data.

    Returns:
        HttpResponse: Form for upload or redirect to home on success.
    """
    if request.method == 'POST':
        form = UpcomingBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UpcomingBookForm()
    return render(request, 'books/upload_upcoming_book.html', {'form': form})


def upcoming_book_detail(request, pk):
    """
    Show detailed view of a specific upcoming book.

    Args:
        request (HttpRequest): The HTTP request.
        pk (int): Primary key of the upcoming book.

    Returns:
        HttpResponse: Rendered detail view of the upcoming book.
    """
    book = get_object_or_404(UpcomingBook, pk=pk)
    return render(request, 'books/upcoming_book_detail.html', {'book': book})


def upcoming_books(request):
    """
    Display a full list of upcoming book releases.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Rendered list view of all upcoming books.
    """
    upcoming_books = UpcomingBook.objects.all()
    return render(request, 'books/upcoming_books.html', {'upcoming_books': upcoming_books})
