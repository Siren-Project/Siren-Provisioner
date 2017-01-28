From hypriot/armhf-busybox

RUN mkdir /www
RUN ls
ADD video.mp4 /www/
ADD index.html /www/
CMD /bin/busybox httpd -f -p 80 -h /www
EXPOSE 80