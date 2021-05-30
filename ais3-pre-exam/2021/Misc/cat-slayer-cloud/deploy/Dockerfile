FROM python:3.8

RUN pip install pycryptodome
RUN apt-get update
RUN apt-get install xinetd -qy
RUN useradd -m cat_slayer_cloud
COPY ./share /home/cat_slayer_cloud
COPY ./xinetd /etc/xinetd.d/cat_slayer_cloud
COPY ./flag "/#h3y_I'm_the_fl4ggg#"
RUN chown -R root:root /home/cat_slayer_cloud
RUN chmod -R 755 /home/cat_slayer_cloud

CMD ["/usr/sbin/xinetd","-dontfork"]