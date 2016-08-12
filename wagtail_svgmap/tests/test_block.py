import json

from django.utils.encoding import force_text

import pytest
from wagtail.wagtailcore.fields import StreamField
from wagtail_svgmap.blocks import ImageMapBlock
from wagtail_svgmap.models import ImageMap

stream_field = StreamField([
    ('imagemap', ImageMapBlock()),
])


@pytest.mark.django_db
def test_id_caching(example_svg_doc):
    map = ImageMap.objects.create(svg=example_svg_doc)
    map.regions.create(element_id='green', link_external='/foobar', target='_blank')
    serialized_field_content = json.dumps(
        # This is empirically what is saved for a streamfield of the above ilk
        [{'type': 'imagemap', 'value': {'map': map.pk, 'css_class': 'huijui'}}]
    )
    stream_content = force_text(stream_field.to_python(serialized_field_content))
    assert 'huijui' in stream_content
    assert '/foobar' in stream_content
    assert 'green' in stream_content