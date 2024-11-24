from openai import OpenAI
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)

base_url = ut.ENV["AI_URL"]
api_key = ut.ENV["AI_TOKEN"]
model = ut.ENV["AI_MODEL"]

client = OpenAI(base_url=base_url, api_key=api_key)

system_prompt = ut.ENV.get("SYSTEM_PROMPT", None)


def default_system_prompt(source_lang=None, target_lang="English"):
    return " ".join([
        "You are a professional translator.",
        f"please translate the following into {target_lang}," if not source_lang or source_lang.lower() == "auto"
        else f"please translate the following in {source_lang} into {target_lang},",
        "do not give any text other than the translated content,",
        "and trim the spaces at the end:"
    ])


def get_system_prompt(source_lang=None, target_lang="English"):
    if system_prompt:
        return system_prompt.replace("{source_lang}", source_lang).replace("{target_lang}", target_lang)
    return default_system_prompt(source_lang, target_lang)


def translate_text(text, source_lang=None, target_lang="English"):
    completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
            {"role": "system", "content": get_system_prompt(
                source_lang, target_lang)},
            {"role": "user", "content": text}
        ]
    )
    return completion.choices[0].message.content


if __name__ == "__main__":
    print(model)
    text = "Deux hommes, âgés respectivement de 22 et 28 ans, et une femme de 22 ans ont été arrêtés pour entrave du travail des policiers, a indiqué Véronique Dubuc, porte-parole du SPVM. La femme sera aussi accusée de voie de fait. Tous ont été identifiés et libérés sur les lieux. Ils devront éventuellement comparaître pour répondre des accusations."
    print(text)
    translated_text = translate_text(
        text, source_lang="French", target_lang="English")
    print(f"Translated text: {translated_text}")
    translated_text = translate_text(
        text, source_lang="French", target_lang="Simple Chinese")
    print(f"Translated text: {translated_text}")
