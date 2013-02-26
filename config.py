import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
    jerry = dict(key="agxkZXZ-ai1lcnJpY29yEAsSCUFwcEFjY2VzcxjpBww",
            secret=None)
else:
    jerry = dict(key="agpzfmotZXJyaWNvcg8LEglBcHBBY2Nlc3MYAQw",
            secret=None)

