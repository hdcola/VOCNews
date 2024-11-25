from openai import OpenAI
import utils as ut
from logging_conf import logger

log = logger.getChild(__name__)

# Initialize OpenAI configuration
base_url = ut.ENV.get('AI_URL', '')
api_key = ut.ENV.get('AI_TOKEN', '')
model = ut.ENV.get('AI_MODEL', '')

try:
    client = OpenAI(base_url=base_url, api_key=api_key)
except Exception as e:
    log.error(f"Failed to initialize OpenAI client: {e}")
    raise

system_prompt = ut.ENV.get("SYSTEM_PROMPT", None)


def default_system_prompt(source_lang=None, target_lang="English") -> str:
    """Generate default system prompt for translation.

    Args:
        source_lang (str, optional): Source language. Defaults to None.
        target_lang (str, optional): Target language. Defaults to "English".

    Returns:
        str: Formatted system prompt for translation
    """
    return " ".join([
        "You are a professional translator.",
        f"please translate the following into {target_lang}," if not source_lang or source_lang.lower() == "auto"
        else f"please translate the following in {source_lang} into {target_lang},",
        "do not give any text other than the translated content,",
        "and trim the spaces at the end:"
    ])


def get_system_prompt(source_lang=None, target_lang="English") -> str:
    """Get system prompt for translation, using custom prompt if available.

    Args:
        source_lang (str, optional): Source language. Defaults to None.
        target_lang (str, optional): Target language. Defaults to "English".

    Returns:
        str: System prompt to use for translation
    """
    if system_prompt:
        return system_prompt.replace("{source_lang}", source_lang).replace("{target_lang}", target_lang)
    return default_system_prompt(source_lang, target_lang)


def translate_text(text: str, source_lang=None, target_lang="English") -> str:
    """Translate text using OpenAI API.

    Args:
        text (str): Text to translate
        source_lang (str, optional): Source language. Defaults to None.
        target_lang (str, optional): Target language. Defaults to "English".

    Returns:
        str: Translated text

    Raises:
        Exception: If translation fails
    """
    try:
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
    except Exception as e:
        log.error(f"Translation failed: {e}")
        raise


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
