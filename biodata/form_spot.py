from django import forms
from .models import SpotAdvanceBookletBooking

class AdvanceBookletBookingForm(forms.ModelForm):
    class Meta:
        model = SpotAdvanceBookletBooking
        fields = [
            'name',
            'city',
            'whatsapp_number',
            'email',
            'girls_booklet_with',
            'boys_booklet_with',
            'courier_address',
            'payment_screenshot',
            # Removed 'total_amount' from fields as it is calculated in backend
        ]
        widgets = {
            'courier_address': forms.TextInput(attrs={'placeholder': 'Enter courier address'}),
            # Removed total_amount widget since field removed
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['name', 'city', 'whatsapp_number', 'email', 'payment_screenshot', 'courier_address']
        for field_name in self.fields:
            self.fields[field_name].required = field_name in required_fields

    def clean(self):
        cleaned_data = super().clean()
        girls_booklet_with = cleaned_data.get('girls_booklet_with')
        boys_booklet_with = cleaned_data.get('boys_booklet_with')
        courier_address = cleaned_data.get('courier_address')

        # At least one booklet type must be chosen
        if not (girls_booklet_with or boys_booklet_with):
            raise forms.ValidationError("Please select at least one booklet type (Girls/Boys).")

        # Courier address required
        if not courier_address:
            self.add_error('courier_address', 'Courier address is required.')

        # Calculate total: ₹500 per booklet + ₹100 courier charge (if at least one selected)
        total = 0
        price_per_booklet = 500
        courier_charge = 0
        selected = 0
        if girls_booklet_with:
            total += price_per_booklet
            selected += 1
        if boys_booklet_with:
            total += price_per_booklet
            selected += 1
        if selected > 0:
            total += courier_charge
        cleaned_data['total_amount'] = total

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # instance.with_courier = True  # Remove this as with_courier field does not exist
        # Set total_amount from cleaned_data calculated value
        if 'total_amount' in self.cleaned_data:
            instance.total_amount = self.cleaned_data['total_amount']
        if commit:
            instance.save()
        return instance
