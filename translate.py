from googletrans import Translator as GoogleTranslator

translator = GoogleTranslator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
      'translate.google.cn'
    ])

def translate(input_txt, dest):
    translation = translator.translate(input_txt, dest=dest)
    # print(translate)
    return translation