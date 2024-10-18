from django import forms
from formtools.wizard.views import SessionWizardView
from cards.models import Set, Card, CardRarity


class AskForExtension(forms.Form):
    set_id = forms.CharField(label="Id of the pokemon set")
