FROM java:8-jre AS maven-builder

RUN echo "deb http://mirrors.aliyun.com/debian/ jessie main non-free contrib" > /etc/apt/sources.list \
	&& echo "deb http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib" >> /etc/apt/sources.list \
	&& echo "deb-src http://mirrors.aliyun.com/debian/ jessie main non-free contrib" >> /etc/apt/sources.list \
	&& echo "deb-src http://mirrors.aliyun.com/debian/ jessie-proposed-updates main non-free contrib" >> /etc/apt/sources.list

RUN apt-get -y update && apt-get -y install git \
    && apt-get -y clean all

# Get cas-overlay
RUN cd / \
    && git clone -b 5.3 --depth 1 --single-branch https://github.com/apereo/cas-overlay-template.git cas-overlay \
    && chmod 750 /cas-overlay/mvnw

ADD build-config/pom.xml /cas-overlay/pom.xml

RUN cd /cas-overlay && ./mvnw clean package -T 10



FROM java:8-jre-alpine

COPY --from=maven-builder /cas-overlay/target/cas.war cas.war

ADD keys/cas.keystore /etc/cas/thekeystore
ADD etc/ /etc/cas/config
ADD services/ /etc/cas/services

EXPOSE 8080 8443

CMD ["java", "-jar", "cas.war"]