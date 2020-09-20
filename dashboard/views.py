from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from profiles.models import User
from checkout.models import Order
from games.models import Game
from .forms import GameForm
from django.contrib.admin.models import LogEntry
from decimal import Decimal
from django.db.models import Q


@login_required
def dashboard(request):
    """
   renders the main admin dashboard
    """

    # redirect to home if not superuser
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admin uses can do that.")
        return redirect(reverse("home"))

    # log entry src https://stackoverflow.com/questions/5746624/showing-django-admin-actions-on-template
    logs = LogEntry.objects.select_related().all().order_by("-id")[:5]

    all_games = Game.objects.all()
    all_users = User.objects.all()
    all_orders = Order.objects.all()

    total_sales = Decimal(0)
    for order in all_orders:
        total_sales += order.grand_total

    context = {
        "logs": logs,
        "all_games": all_games,
        "all_orders": all_orders,
        "total_sales": total_sales,
        "all_users": all_users,
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
def add_game(request):
    """
    Renders a view to add a product to the database
    """
    # redirect to home if not superuser
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admin uses can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES)
        if game_form.is_valid():
            game = game_form.save()
            messages.success(request, "Successfully added the Game!")
            return redirect(reverse("game_detail", args=[game.id]))
        else:
            messages.error(
                request, "Failed to add the Game. Please ensure the form is valid!"
            )
    else:
        game_form = GameForm()

    context = {
        "game_form": game_form,
    }
    return render(request, "dashboard/add_game.html", context)


@login_required
def edit_game(request, game_id):
    """ Edit game in database """

    # redirect to home if not superuser
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admin uses can do that.")
        return redirect(reverse("home"))

    game = get_object_or_404(Game, pk=game_id)

    if request.method == "POST":
        game_form = GameForm(request.POST, request.FILES, instance=game)
        if game_form.is_valid():
            game = game_form.save()
            messages.success(request, f"Successfully updated {game.name}!")
            return redirect(reverse("game_detail", args=[game.id]))
        else:
            messages.error(
                request, "Failed to update the Game. Please ensure the form is valid!"
            )
    else:
        game_form = GameForm(instance=game)
        messages.info(request, f"you are now editing {game.name}!")

    template = "dashboard/edit_game.html"
    context = {
        "game_form": game_form,
        "game": game,
    }

    return render(request, template, context)


@login_required
def delete_game(request, game_id):
    """ Delete game in database """

    # redirect to home if not superuser
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only admin uses can do that.")
        return redirect(reverse("home"))

    game = get_object_or_404(Game, pk=game_id)
    game.delete()
    messages.success(request, "Game deleted!")
    return redirect(reverse("dashboard"))


@login_required
def games_management(request):
    """ Game management view """
    all_games = Game.objects.all()
    all_games = all_games.order_by('name')
    search_term = None
    # check if it is a search query
    if "q" in request.GET:
        query = request.GET["q"]
        search_term = query
        # If the user has not entered any text display an error
        if not query:
            messages.error(request, "No search text entered!")
            return redirect(reverse("games_management"))

        # filter search based on name
        all_games = all_games.filter(Q(name__icontains=query))


    context = {
        "all_games": all_games,
        "search_term": search_term,
    }

    return render(request, "dashboard/games_management.html", context)
