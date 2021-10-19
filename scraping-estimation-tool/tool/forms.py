from django import forms


class JavascriptForm(forms.Form):
	domain = forms.CharField(label='Domain', max_length=200)
	url_label = forms.CharField(label='URL', max_length=1000)
	xpath_box = forms.CharField(label='xpath_list')