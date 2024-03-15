#!/usr/bin/env python
# -*- coding: <encoding name> -*-

# 【文件作用】 迁移给定git仓库url到gitea服务

from pathlib import Path
import re

import httpx

import sys
sys.path.append("/fridaAnlzAp/github-gitee-gitea/py_util/")

from GitRepoUrlParser import gitMirrorRepoUrlParseF,gitRepoUrlParseF

def giteaMigrateApi(repoUrl:str,mirrorBaseUrl,mirrorOrg,giteaBaseUrl:str,giteaToken:str):
  repo_url=gitRepoUrlParseF(repoUrl)

  """
  curl -X 'POST' \
  'https://github.local/api/v1/orgs?token=ab2a90dc37210a4f9aee91ab959bfa3fc1f6ba6a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "NVlabs",
  "repo_admin_change_team_access": true,
  "visibility": "public"
}'
"""

  newOrg_url=f'{giteaBaseUrl}/api/v1/orgs?token={giteaToken}'
  newOrg_reqBodyDct={
    "username": repo_url.orgName,
  }
  newOrg_resp=httpx.post(url=newOrg_url,json=newOrg_reqBodyDct,verify=False)
  newOrg_ok=newOrg_resp.status_code==422 or newOrg_resp.is_success #422 gitea 已经存在组织
  if(not newOrg_ok):
    newOrg_msg=f"创建gitea组织失败，【${newOrg_resp.status_code}, ${newOrg_resp.text}】"
    print(newOrg_msg)
    return False
  

  """
  curl -k -X 'POST' \
    'https://github.local/api/v1/repos/migrate?token=b1d490eaf6b88a6c37bd482d8e05e3a0061f066c' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "clone_addr": "https://gitee.com/mirrr/NVlabs--cub.git",
    "repo_name": "cub",
    "repo_owner": "NVlabs"
  }'

  """

  mirrorRepoUrl=repo_url.to_mirror_url(mirrorBaseUrl,mirrorOrg)
  mirrRepo_url:str = mirrorRepoUrl.url_str()
  migrate_url=f'{giteaBaseUrl}/api/v1/repos/migrate?token={giteaToken}'
  reqBodyDct={
      "clone_addr": mirrRepo_url,
    "repo_owner": repo_url.orgName,
    "repo_name": repo_url.repoName
  }
  resp=httpx.post(url=migrate_url,json=reqBodyDct,verify=False)
  msg=f"【gitea迁移接口响应】状态码【{resp.status_code}】，响应文本【{resp.text}】\n 【迁移仓库】【{repoUrl}】--->【{mirrRepo_url}】"
  ok= resp.status_code == 409 or resp.is_success #409 gitea 已经存在仓库
  msg=f'{"迁移成功" if ok else "迁移失败" }，{msg}'
  print(msg)
  return ok