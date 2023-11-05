# WAV2LIP Server

## how to use

- publish task

  ```bash
  curl --location 'http://sanyihe.tpddns.cn:7861/project/create' \
  --form 'video=@"/Users/ren/Downloads/27_1697104538.mp4"' \
  --form 'template_id="-1"' \
  --form 'speech=@"/Users/ren/github/wav2lip_server/test/熵.WAV"'
  ```
- get task result

  ```bash
  curl --location 'http://sanyihe.tpddns.cn:7861/project/1' 
  ```

## Project link

[renz7/wav2lip](https://github.com/Renz7/wav2lip_server.git)
