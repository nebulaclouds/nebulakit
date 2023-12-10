def get_default_success_html(endpoint: str) -> str:
    return f"""
<html>
    <head>
            <title>OAuth2 Authentication Success</title>
    </head>
    <body>
            <h1>Successfully logged into {endpoint}</h1>
            <img height="100" src="https://artwork.lfaidata.foundation/projects/nebula/horizontal/color/nebula-horizontal-color.svg" alt="Nebula login"></img>
    </body>
</html>
"""  # noqa
