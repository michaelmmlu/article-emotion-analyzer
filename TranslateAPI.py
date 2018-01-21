"""Detects the text's language."""
from google.cloud import translate
translate_client = translate.Client()

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
print "Enter message:"
text = input()
result = translate_client.detect_language(text)

print('Text: {}'.format(text))
print('Confidence: {}'.format(result['confidence']))
print('Language: {}'.format(result['language']))
