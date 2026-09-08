from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import yt_dlp


def send_json(handler, status, data):
    body = json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ).encode("utf-8")

    handler.send_response(status)
    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
    )
    handler.send_header(
        "Access-Control-Allow-Origin",
        "*"
    )
    handler.send_header(
        "Access-Control-Allow-Methods",
        "GET, OPTIONS"
    )
    handler.send_header(
        "Access-Control-Allow-Headers",
        "Content-Type"
    )
    handler.send_header(
        "Content-Length",
        str(len(body))
    )
    handler.end_headers()
    handler.wfile.write(body)


def get_formats(info):
    result = []

    for fmt in info.get("formats", []):
        url = fmt.get("url")

        if not url:
            continue

        result.append({
            "format_id": fmt.get("format_id"),
            "ext": fmt.get("ext"),
            "resolution": fmt.get("resolution"),
            "width": fmt.get("width"),
            "height": fmt.get("height"),
            "fps": fmt.get("fps"),
            "filesize": fmt.get("filesize"),
            "filesize_approx": fmt.get(
                "filesize_approx"
            ),
            "vcodec": fmt.get("vcodec"),
            "acodec": fmt.get("acodec"),
            "audio_only": (
                fmt.get("vcodec") == "none"
                and fmt.get("acodec") != "none"
            ),
            "video_only": (
                fmt.get("vcodec") != "none"
                and fmt.get("acodec") == "none"
            ),
            "download_url": url
        })

    return result


def choose_best(formats):
    combined = [
        f for f in formats
        if not f["video_only"]
        and not f["audio_only"]
    ]

    if not combined:
        return None

    return max(
        combined,
        key=lambda f: (
            f.get("height") or 0,
            f.get("width") or 0,
            f.get("fps") or 0
        )
    )


def extract(url):

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(
            url,
            download=False
        )

    formats = get_formats(info)
    best = choose_best(formats)

    return {
        "success": True,

        "platform": info.get(
            "extractor_key"
        ),

        "id": info.get("id"),

        "title": info.get("title"),

        "description": info.get(
            "description"
        ),

        "thumbnail": info.get(
            "thumbnail"
        ),

        "duration": info.get(
            "duration"
        ),

        "uploader": info.get(
            "uploader"
        ),

        "uploader_id": info.get(
            "uploader_id"
        ),

        "webpage_url": info.get(
            "webpage_url"
        ),

        "original_url": url,

        "best": best,

        "formats": formats
    }


class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):

        send_json(
            self,
            200,
            {
                "success": True
            }
        )

    def do_GET(self):

        try:

            parsed = urlparse(
                self.path
            )

            params = parse_qs(
                parsed.query
            )

            url = params.get(
                "url",
                [None]
            )[0]

            if not url:

                send_json(
                    self,
                    400,
                    {
                        "success": False,
                        "error": "Missing URL",
                        "usage":
                            "/api/download?url=VIDEO_URL"
                    }
                )

                return

            if not url.startswith(
                ("http://", "https://")
            ):

                send_json(
                    self,
                    400,
                    {
                        "success": False,
                        "error": "Invalid URL"
                    }
                )

                return

            data = extract(url)

            send_json(
                self,
                200,
                data
            )

        except Exception as error:

            send_json(
                self,
                500,
                {
                    "success": False,
                    "error": str(error)
                }
            )
