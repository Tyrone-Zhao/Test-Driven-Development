from django import forms
from django.core.exceptions import ValidationError

from lists.models import Item, List


EMPTY_ITEM_ERROR = "请不要输入空的待办事项"
DUPLICATE_ITEM_ERROR = "此待办事项已存在"


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


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(
                first_item_text=self.cleaned_data["text"],
                owner=owner
            )
        else:
            return List.create_new(
                first_item_text=self.cleaned_data["text"],
            )


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {"text": [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
