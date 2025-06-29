from django import forms

class AdvancePassBookingForm(forms.Form):
    name = forms.CharField(max_length=255, required=True, label="Your Name")
    city = forms.CharField(max_length=255, required=True, label="Your City")
    whatsapp_number = forms.CharField(max_length=20, required=True, label="Your WhatsApp Number")
    email = forms.EmailField(required=True, label="Your Email ID")

    entry_token_selected = forms.BooleanField(required=False, label="Entry Token Pass : Rs 20")
    entry_token_quantity = forms.ChoiceField(
        choices=[('0', '0')] + [(str(i), str(i)) for i in range(1, 11)],
        required=False,
        label="Quantity for Entry Token Pass"
    )

    tea_coffee_selected = forms.BooleanField(required=False, label="Tea - Coffee Pass : Rs 30 (Morning + Evening included)")
    tea_coffee_quantity = forms.ChoiceField(
        choices=[('0', '0')] + [(str(i), str(i)) for i in range(1, 11)],
        required=False,
        label="Quantity for Tea - Coffee Pass"
    )

    unlimited_buffet_selected = forms.BooleanField(required=False, label="Unlimited Buffet Lunch : Rs 200")
    unlimited_buffet_quantity = forms.ChoiceField(
        choices=[('0', '0')] + [(str(i), str(i)) for i in range(1, 11)],
        required=False,
        label="Quantity for Unlimited Buffet Lunch"
    )

    payment_screenshot = forms.ImageField(required=False, label="Attach Your Payment Success Screenshot")

    def clean_whatsapp_number(self):
        number = self.cleaned_data.get('whatsapp_number')
        if number and not number.isdigit():
            raise forms.ValidationError("WhatsApp number must contain only digits.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        entry_token_selected = cleaned_data.get('entry_token_selected')
        entry_token_qty = int(cleaned_data.get('entry_token_quantity', '0') or '0')
        tea_coffee_selected = cleaned_data.get('tea_coffee_selected')
        tea_coffee_qty = int(cleaned_data.get('tea_coffee_quantity', '0') or '0')
        unlimited_buffet_selected = cleaned_data.get('unlimited_buffet_selected')
        unlimited_buffet_qty = int(cleaned_data.get('unlimited_buffet_quantity', '0') or '0')

        if not (entry_token_selected or tea_coffee_selected or unlimited_buffet_selected):
            raise forms.ValidationError("Please select at least one pass type.")

        if entry_token_selected and entry_token_qty == 0:
            self.add_error('entry_token_quantity', 'Please select quantity for Entry Token Pass.')

        if tea_coffee_selected and tea_coffee_qty == 0:
            self.add_error('tea_coffee_quantity', 'Please select quantity for Tea - Coffee Pass.')

        if unlimited_buffet_selected and unlimited_buffet_qty == 0:
            self.add_error('unlimited_buffet_quantity', 'Please select quantity for Unlimited Buffet Lunch.')

        return cleaned_data
