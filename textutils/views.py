from django.http import HttpResponse
from django.shortcuts import render
from textblob import TextBlob
from langdetect import detect
# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer
# import nltk
# nltk.download('punkt')
from transformers import pipeline

def summarize_text(text):
    summarizer = pipeline("summarization")
    try:
        summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"An error occurred: {str(e)}"

def index(request):
    return render(request, 'index.html')

def analyze(request):
    # Get the text
    djtext = request.POST.get('text', 'default')

    # Check checkbox values
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    numberremover = request.POST.get('numberremover', 'off')
    sentiment_analysis = request.POST.get('sentiment_analysis', 'off')
    language_detection = request.POST.get('language_detection', 'off')
    text_summarization = request.POST.get('text_summarization', 'off')

    # Initialize the analyzed variable
    analyzed = djtext

    # Text processing logic
    if removepunc == "on":
        punctuations = '''!()-[]}{;:,'\"<>./?@#$%^&*_~'''
        analyzed = "".join([char for char in djtext if char not in punctuations])
        djtext = analyzed

    if fullcaps == "on":
        analyzed = djtext.upper()
        djtext = analyzed

    if extraspaceremover == "on":
        analyzed = " ".join(djtext.split())
        djtext = analyzed

    if newlineremover == "on":
        analyzed = djtext.replace("\n", "").replace("\r", "")
        djtext = analyzed

    if numberremover == "on":
        analyzed = "".join([char for char in djtext if not char.isdigit()])
        djtext = analyzed

    # Machine Learning-based features
    if sentiment_analysis == "on":
        blob = TextBlob(djtext)
        sentiment = blob.sentiment.polarity
        sentiment_text = f"Sentiment Polarity: {sentiment:.2f}"
        params = {'purpose': 'Sentiment Analysis', 'analyzed_text': sentiment_text}
        return render(request, 'analyze.html', params)

    if language_detection == "on":
        language = detect(djtext)
        language_text = f"Detected Language: {language}"
        params = {'purpose': 'Language Detection', 'analyzed_text': language_text}
        return render(request, 'analyze.html', params)

    if text_summarization == "on":
        summary = summarize_text(djtext)
        params = {'purpose': 'Text Summarization', 'analyzed_text': summary}
        return render(request, 'analyze.html', params)

    if removepunc != "on" and newlineremover != "on" and extraspaceremover != "on" and fullcaps != "on" and numberremover != "on" and sentiment_analysis != "on" and language_detection != "on" and text_summarization != "on":
        return HttpResponse("Please select at least one operation and try again.")

    params = {'purpose': 'Text Analysis', 'analyzed_text': analyzed}
    return render(request, 'analyze.html', params)

def about(request):
    return render(request, 'about.html')
