from django.shortcuts import render

# Create your views here.
import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'translator/translator.html')

def translator_app(request):
    return render(request, 'translator/translator.html')

@csrf_exempt
@require_POST
def translate(request):
    data = json.loads(request.body)
    text = data.get('text', '').strip()
    source_lang = data.get('source_lang', 'auto')
    target_lang = data.get('target_lang', 'hi')

    if not text:
        return JsonResponse({'error': 'No text provided'}, status=400)

    # API 1: MyMemory
    try:
        lang_pair = target_lang if source_lang == 'auto' else f"{source_lang}|{target_lang}"
        resp = requests.get(
            'https://api.mymemory.translated.net/get',
            params={'q': text, 'langpair': lang_pair},
            timeout=5
        )
        result = resp.json()
        if result.get('responseStatus') == 200:
            return JsonResponse({'translation': result['responseData']['translatedText']})
    except Exception:
        pass

    # API 2: LibreTranslate
    try:
        resp = requests.post(
            'https://libretranslate.de/translate',
            json={'q': text, 'source': source_lang, 'target': target_lang, 'format': 'text'},
            timeout=5
        )
        result = resp.json()
        if result.get('translatedText'):
            return JsonResponse({'translation': result['translatedText']})
    except Exception:
        pass

    return JsonResponse({'error': 'All server-side APIs failed'}, status=503)