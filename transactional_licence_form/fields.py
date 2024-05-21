from django import forms


class FCLFieldMixin(object):
    def __init__(self, *args, **kwargs):
        self.send_to_dynamics = kwargs.pop("send_to_dynamics", True)
        super(FCLFieldMixin, self).__init__(*args, **kwargs)


class FCLOtherField(forms.TextInput):
    template_name = "widgets/other_field.html"


class FCLCheckboxWidgetWithOthers(forms.MultiWidget):
    template_name = "widgets/checkbox_with_others.html"

    def __init__(self, choices_field, other_fields, attrs=None):
        self.choices_field = choices_field
        self.other_fields = {}
        other_widgets = {}
        for ix, (option_pos, f) in enumerate(other_fields.items()):
            widget = FCLOtherField()
            field = f["field"]
            name = f["name"]
            self.other_fields[option_pos] = {
                "name": name,
                "field": field,
                "widget": widget,
                "field_index": ix,
            }
            other_widgets[name] = widget

        self.choice_widget = forms.CheckboxSelectMultiple(attrs)
        widgets = {**{"choices": self.choice_widget}, **other_widgets}
        super(FCLCheckboxWidgetWithOthers, self).__init__(widgets, attrs)

    def get_context(self, name, value, attrs):
        context = super(FCLCheckboxWidgetWithOthers, self).get_context(
            name, value, attrs
        )
        context["field"] = self.choices_field
        context["other_fields"] = self.other_fields
        context["other_field_subwidgets"] = {}
        for key, field in self.other_fields.items():
            ix = field["field_index"]
            # We add 1 here as the checkbox widget itself is always the first subwidget
            subwidget = context["widget"]["subwidgets"][ix + 1]
            context["other_field_subwidgets"][key] = subwidget
        return context

    def decompress(self, value=None):
        if value is None:
            value = {}
        choices = value.get("choices", [])
        others = []
        for field in self.other_fields.values():
            others.insert(field["field_index"], value.get(field["name"], None))
        return [choices] + others


class FCLCharField(FCLFieldMixin, forms.CharField):
    pass


class FCLEmailField(FCLFieldMixin, forms.EmailField):
    pass


class FCLChoiceField(FCLFieldMixin, forms.ChoiceField):
    widget = forms.RadioSelect


class FCLMultipleChoiceField(FCLFieldMixin, forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class FCLMultipleChoiceFieldWithOthers(FCLFieldMixin, forms.MultiValueField):
    def __init__(self, **kwargs):
        choices = kwargs.pop("choices")
        self.other_fields = {}
        for field_index, (opt_index, name) in enumerate(
            kwargs.pop("other_fields", {}).items()
        ):
            self.other_fields[opt_index] = {
                "name": name,
                "field": FCLCharField(max_length=50, required=False),
                "field_index": field_index,
            }
        self.choices_field = FCLMultipleChoiceField(
            choices=choices, required=True, label=False
        )
        self.widget = FCLCheckboxWidgetWithOthers(self.choices_field, self.other_fields)
        fields = [self.choices_field] + [d["field"] for d in self.other_fields.values()]
        super(FCLMultipleChoiceFieldWithOthers, self).__init__(
            fields, **kwargs, require_all_fields=False
        )

    def compress(self, values=None):
        if values is None or len(values) == 0:
            values = [None]
        choices, *others = values
        compressed = {"choices": choices if choices else []}
        for field in self.other_fields.values():
            try:
                compressed[field["name"]] = others[field["field_index"]]
            except IndexError:
                pass
        return compressed
