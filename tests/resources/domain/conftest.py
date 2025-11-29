import pytest

from modules.resources.domain.entities import Resource


@pytest.fixture
def resources() -> list[Resource]:
    return [
        Resource.Builder()
        .with_name('Random Image 1')
        .with_url('https://picsum.photos/200/200')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Image 2')
        .with_url('https://picsum.photos/200/200')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Video 1')
        .with_url('https://www.youtube.com/watch?v=1')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Video 2')
        .with_url('https://www.youtube.com/watch?v=2')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Audio 1')
        .with_url('https://example.com/audio1.mp3')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Audio 2')
        .with_url('https://example.com/audio2.mp3')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Text 1')
        .with_url('https://example.com/text1.txt')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Text 2')
        .with_url('https://example.com/text2.txt')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Other 1')
        .with_url('https://example.com/other1')
        .with_type('image')
        .build(),
        Resource.Builder()
        .with_name('Random Other 2')
        .with_url('https://example.com/other2')
        .with_type('image')
        .build(),
    ]
