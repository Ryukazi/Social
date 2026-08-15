# ⚡ Social Downloader API

A Vercel-hosted media extraction API powered by yt-dlp.

## Features

- YouTube / not working 
- TikTok
- Instagram
- Facebook
- X/Twitter
- Twitch
- Pinterest video 
- Other yt-dlp supported sites

## API

GET:

/api/download?url=VIDEO_URL

Example:

https://social-chi-amber.vercel.app/api/download?url=https://www.instagram.com/reel/DbpQKueyONq/?igsh=MTB4Nm9xcjZxbnVzcw==&igsi=MTB4Nm9xcjZxbnVzcw==

## Response

The API returns:

- platform
- title
- thumbnail
- uploader
- duration
- available formats
- direct media URLs when available

## Deploy

Push this repository to GitHub.

Then import the repository into Vercel.

Vercel automatically installs the Python dependencies from requirements.txt.

## Important

Media URLs returned by social platforms may expire.

Some websites require authentication or may block automated extraction.

Only download content you have permission to download.
# Social
