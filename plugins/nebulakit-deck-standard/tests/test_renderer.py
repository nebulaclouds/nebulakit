import datetime
import tempfile

import markdown
import pandas as pd
import pytest
from nebulakitplugins.deck.renderer import (
    BoxRenderer,
    FrameProfilingRenderer,
    GanttChartRenderer,
    ImageRenderer,
    MarkdownRenderer,
    TableRenderer,
)
from PIL import Image

from nebulakit.types.file import NebulaFile, JPEGImageFile, PNGImageFile

df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [1, 22]})
time_info_df = pd.DataFrame(
    [
        dict(
            Name="foo",
            Start=datetime.datetime.utcnow(),
            Finish=datetime.datetime.utcnow() + datetime.timedelta(microseconds=1000),
            WallTime=1.0,
            ProcessTime=1.0,
        )
    ]
)


def test_frame_profiling_renderer():
    renderer = FrameProfilingRenderer()
    assert "Pandas Profiling Report" in renderer.to_html(df).title()


def test_markdown_renderer():
    md_text = "#Hello Nebula\n##Hello Nebula\n###Hello Nebula"
    renderer = MarkdownRenderer()
    assert renderer.to_html(md_text) == markdown.markdown(md_text)


def test_box_renderer():
    renderer = BoxRenderer("Name")
    assert "Plotlyconfig = {Mathjaxconfig: 'Local'}" in renderer.to_html(df).title()


def create_simple_image(fmt: str):
    """Create a simple PNG image using PIL"""
    img = Image.new("RGB", (100, 100), color="black")
    tmp = tempfile.mktemp()
    img.save(tmp, fmt)
    return tmp


png_image = create_simple_image(fmt="png")
jpeg_image = create_simple_image(fmt="jpeg")


@pytest.mark.parametrize(
    "image_src",
    [
        NebulaFile(path=png_image),
        JPEGImageFile(path=jpeg_image),
        PNGImageFile(path=png_image),
        Image.open(png_image),
    ],
)
def test_image_renderer(image_src):
    renderer = ImageRenderer()
    assert "<img" in renderer.to_html(image_src)


def test_table_renderer():
    renderer = TableRenderer()
    assert "Dataframe Table-Class" in renderer.to_html(time_info_df).title()


def test_gantt_chart_renderer():
    renderer = GanttChartRenderer()
    assert "Plotlyconfig = {Mathjaxconfig: 'Local'}" in renderer.to_html(time_info_df).title()
