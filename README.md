# ⚡ Social Downloader API

A Vercel-hosted media extraction API powered by yt-dlp.

## Features

- YouTube / not working 
- TikTok
- Instagram
- Facebook
- X/Twitter / haven't checked 
- Reddit / haven't checked
- Vimeo / haven't checked
- Twitch / haven't checked
- Pinterest video 
- Other yt-dlp supported sites

## API

GET:

/api/download?url=VIDEO_URL

Example:

/api/download?url=https://www.youtube.com/watch?v=VIDEO_ID

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
