# Stream Recorder

## About this project

Python script based streaming downloader(recorder) for china mainland live streamings.

It's aiming for running in background and download the stream when the stream is available.

## Usage

```bash
python bilibili.py roomId [path]
```
If the _path_ parameter is not specified, download path would be the current path.

### Windows

Try pythonw to make the script run at background for now.
```batch
pythonw bilibili.py roomId [path]
```

## Todo List

- [ ] Error handling.
- [ ] Native service implement (makes script run at background) for Windows.
- [ ] Native service implement for Linux.
- [ ] Logs output.

## Author

HLM319

## License

GNU LGPL-v2.1-only