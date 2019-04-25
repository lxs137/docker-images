FROM fluent/fluentd:v1.4.2-1.0

# Use root account to use apk
USER root

RUN apk add --no-cache --update --virtual .build-deps sudo build-base ruby-dev \
    && sudo gem install fluent-plugin-kafka --no-document \
    && sudo gem sources --clear-all \
    && apk del .build-deps \
    && rm -rf /home/fluent/.gem/ruby/2.5.0/cache/*.gem

USER fluent
