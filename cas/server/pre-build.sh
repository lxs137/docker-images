#/bin/bash

if [[ $# -ne 2 || $1 != "-pass" ]]; then
    echo "Error command format: "
    echo "$0 -pass [password]"
    exit
fi

PASSWORD=$2
KEYSTORE_PATH="./keys/cas.keystore"
CERT_PATH="./keys/cas.cert"

DNAME="CN=cas.njuics.cn,OU=NJU,O=ICS,L=NanJing,ST=NanJing,C=NJ"

mkdir -p ./keys

keytool -genkeypair -alias cas -keyalg RSA -validity 3650 -keypass "${PASSWORD}" -storepass "${PASSWORD}" -keystore "${KEYSTORE_PATH}" -dname "${DNAME}" -ext SAN="ip:127.0.0.1"

keytool -exportcert -alias cas -keypass "${PASSWORD}" -storepass "${PASSWORD}" -keystore "${KEYSTORE_PATH}" -file "${CERT_PATH}"
