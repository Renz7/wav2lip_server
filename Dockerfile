FROM renz7/sd-backend-dep

WORKDIR /ruuner
COPY . /ruuner

RUN chmod 755 entrypoint.sh

EXPOSE 8000
VOLUME ./output/

ENTRYPOINT ["./entrypoint.sh"]