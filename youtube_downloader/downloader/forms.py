from django import forms

class YouTubeDownloadForm(forms.Form):
    video_url = forms.URLField(label='YouTube Video URL', widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter YouTube video URL here...',
    }))
