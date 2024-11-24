import pytest
from translate import default_system_prompt


def test_default_system_prompt_no_params():
    prompt = default_system_prompt()
    assert prompt == "You are a professional translator. please translate the following into English, do not give any text other than the translated content, and trim the spaces at the end:"


def test_default_system_prompt_auto_params():
    prompt = default_system_prompt(source_lang="auto", target_lang="auto")
    assert prompt == "You are a professional translator. please translate the following into English, do not give any text other than the translated content, and trim the spaces at the end:"


def test_default_system_prompt_auto_source_lang():
    prompt = default_system_prompt(
        source_lang="auto", target_lang="French")
    assert prompt == "You are a professional translator. please translate the following into French, do not give any text other than the translated content, and trim the spaces at the end:"
