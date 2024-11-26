
import pytest
from datetime import datetime, timedelta
from src.rssutils import get_last_entries, get_new_entries


@pytest.fixture
def sample_entries():
    now = datetime.now()
    return {
        "entries": [
            {
                "title": "Article 1",
                "published": (now - timedelta(hours=2)).isoformat()
            },
            {
                "title": "Article 2",
                "published": (now - timedelta(hours=1)).isoformat()
            },
            {
                "title": "Article 3",
                "published": now.isoformat()
            }
        ]
    }


@pytest.fixture
def empty_rss():
    return {"entries": []}


def test_get_last_entries_with_entries(sample_entries):
    result = get_last_entries(sample_entries)
    assert result is not None
    assert result["title"] == "Article 3"


def test_get_last_entries_empty():
    result = get_last_entries({"entries": []})
    assert result is None


def test_get_last_entries_no_entries_key():
    result = get_last_entries({})
    assert result is None


def test_get_new_entries_with_new_content(sample_entries):
    now = datetime.now()
    new_rss = {
        "entries": [
            {
                "title": "New Article 1",
                "published": (now + timedelta(hours=1)).isoformat()
            },
            {
                "title": "New Article 2",
                "published": (now + timedelta(hours=2)).isoformat()
            }
        ]
    }
    result = get_new_entries(new_rss, sample_entries)
    assert result is not None
    assert len(result) == 2
    assert result[0]["title"] == "New Article 1"
    assert result[1]["title"] == "New Article 2"


def test_get_new_entries_no_new_content(sample_entries):
    now = datetime.now()
    new_rss = {
        "entries": [
            {
                "title": "Old Article",
                "published": (now - timedelta(hours=3)).isoformat()
            }
        ]
    }
    result = get_new_entries(new_rss, sample_entries)
    assert result is None


def test_get_new_entries_with_empty_last_rss(sample_entries):
    result = get_new_entries(sample_entries, {"entries": []})
    assert result == sample_entries["entries"]


def test_get_new_entries_with_empty_new_rss(sample_entries):
    result = get_new_entries({"entries": []}, sample_entries)
    assert result is None


def test_get_new_entries_with_overlap(sample_entries):
    now = datetime.now()
    new_rss = {
        "entries": [
            {
                "title": "Article 2",
                "published": (now - timedelta(hours=1)).isoformat()
            },
            {
                "title": "Article 3",
                "published": now.isoformat()
            },
            {
                "title": "New Article 1",
                "published": (now + timedelta(hours=1)).isoformat()
            },
            {
                "title": "New Article 2",
                "published": (now + timedelta(hours=2)).isoformat()
            }
        ]
    }
    result = get_new_entries(new_rss, sample_entries)
    assert result is not None
    assert len(result) == 3
    assert result[0]["title"] == "Article 3"
    assert result[1]["title"] == "New Article 1"
    assert result[2]["title"] == "New Article 2"
