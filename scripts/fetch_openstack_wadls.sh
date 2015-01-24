#!/usr/bin/env bash
rm -rf openstack
mkdir -p openstack/wadls

SITE_REPO_DIR="openstack-api-site"

pushd openstack
  if [ ! -d "$SITE_REPO_DIR" ]; then
    git clone https://github.com/openstack/api-site $SITE_REPO_DIR
  else
    git -C $SITE_REPO_DIR pull
  fi
  pushd $SITE_REPO_DIR
    mvn clean generate-sources # normalizes all the WADLs
  popd

  cp $SITE_REPO_DIR/api-ref/target/docbkx/html/wadls/*.wadl wadls/
popd
