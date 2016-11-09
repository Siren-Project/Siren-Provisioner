From busybox

RUN mkdir /www
RUN ls
RUN touch /www/index.html
RUN echo "<body style='background-color:#f3dfa2;'><div style=' text-align:center;'><h1> Service Provider A</h1></div></body>" > /www/index.html
CMD /bin/busybox httpd -f -p 80 -h /www
EXPOSE 80
