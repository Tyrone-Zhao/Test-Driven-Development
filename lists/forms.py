from django import forms

from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ("text",)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                "placeholder": "输入一个待办事项",
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            "text": {"required": EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()
