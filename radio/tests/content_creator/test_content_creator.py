from src.content_creator.content_creator import ContentCreator
from src.content_creator.content_creator_instance import create_content_creator


def test_create_content_creator():
    content_creator = create_content_creator()
    assert isinstance(content_creator, ContentCreator)
    assert len(content_creator.channels) > 0
