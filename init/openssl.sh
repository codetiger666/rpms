#!/bin/sh

handle_version() {
  echo $(curl https://api.github.com/repos/openssl/openssl/releases | jq -r '.[].tag_name' | grep '^openssl-3.2.' | head -n1 | sed 's/openssl-//')
}

handle_version
