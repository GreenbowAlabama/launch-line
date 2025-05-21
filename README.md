# Local Development Setup

## 1. Clone the Repository 

```
git clone https://github.com/your-org/your-repo.git
cd your-repo
```

## 2. Configure Environment Variables

Copy the example environment file and update the values:

```
cp env.dev.example .env.dev
```

Then edit `.env.dev` and provide your own MediaMTX server configuration:

```
RTSP_URL=rtsp://your-media-server-ip:8554/live/stream
MEDIA_SERVER=http://your-media-server-ip:8888
```

**Note:** Do not commit `.env.dev` to source control. It is ignored by `.gitignore`.

## 3. Start the App Locally

```
./start-dev.sh
```

This script will:

* Activate the Python virtual environment
* Install dependencies
* Launch the Flask app with RTSP stream detection enabled

You should see console output showing stream connection and YOLO detections.

For help, contact the maintainer or refer to the documentation inside the `docs/` folder (if present).
