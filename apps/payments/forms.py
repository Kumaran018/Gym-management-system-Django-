from django import forms
from .models import Payment
from apps.membership.models import Membership

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['member', 'membership', 'amount', 'payment_method', 'payment_status']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'membership': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Paid Amount ($)'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter memberships to show relevant subscriptions
        self.fields['membership'].queryset = Membership.objects.all().select_related('member__user', 'plan')
