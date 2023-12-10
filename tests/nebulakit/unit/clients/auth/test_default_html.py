from nebulakit.clients.auth.default_html import get_default_success_html


def test_default_html():
    assert (
        get_default_success_html("nebula.org")
        == """
<html>
    <head>
            <title>OAuth2 Authentication Success</title>
    </head>
    <body>
            <h1>Successfully logged into nebula.org</h1>
            <img height="100" src="https://artwork.lfaidata.foundation/projects/nebula/horizontal/color/nebula-horizontal-color.svg" alt="Nebula login"></img>
    </body>
</html>
"""
    )  # noqa
