import time, os, sys
from unidecode import unidecode
from datetime import datetime, timedelta

from IPython import embed
from traitlets.config import get_config

from django.utils.termcolors import colorize
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import timezone, termcolors, dateformat, translation
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Super Django Shell'

    def handle(self, *args, **options):

        User = get_user_model()
        helpers = [
            ("Date", "datetime, timedelta, time"),
            ("django.utils", "timezone, termcolors, dateformat, translation."),
            ("%quickref", "Quick reference."),
            ("User", "Django Auth Model"),
            ("help", "Python's own help system."),
            ("object?", "Details about 'object'"),
            ("object??", "More Details about 'object' "),
        ]
        registered_models = {}
        for model in apps.get_models():
            module = model.__module__
            name = model.__name__
            locals()[name] = model
            try:
                registered_models[module].append(name)
            except:
                registered_models[module] = [name]

        for module in registered_models:
            helpers.append((module, ", ".join(registered_models[module])))

        banner2 = "\n".join(["%s: %s" % (colorize(x, fg="yellow"), y) for x, y in helpers]) + "\n"
        banner = "Hi! \n\n" \
                 "Here some useful shortcuts (Crtl-D to exit):"

        c = get_config()

        c.InteractiveShell.banner1 = banner
        c.InteractiveShell.banner2 = banner2
        c.TerminalInteractiveShell.confirm_exit = False
        c.PromptManager.in_template = '$ '
        c.PromptManager.out_template = '> '

        embed(config=c)

