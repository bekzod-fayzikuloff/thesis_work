from django import forms

from apps.chats.exceptions import PrivateChatAlreadyExistsError
from apps.chats.models import PrivateChat


class PrivateChatForm(forms.ModelForm):
    def clean(self):
        try:
            data = self.cleaned_data
            second_member, first_member = data["second_member"], data["first_member"]
            qs = PrivateChat.objects.filter(first_member=second_member, second_member=first_member)
            for privatechat in qs:
                if privatechat.id != self.instance.id:
                    raise PrivateChatAlreadyExistsError("Chat with same users already exists")
        except PrivateChatAlreadyExistsError:
            raise forms.ValidationError("Chat with same users already exists")
