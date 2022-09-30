## git认证失败

```shell
[root@centos7 script]# git push origin 2.8_cn
fatal: Authentication failed for 'https://gitlab.hillstonenet.com/hspdev/hst/project/script/webui/isop/mx_main.git/'
```

**解决办法**

```shell
# 输入以下命令
git config --system --unset credential.helper
# 然后重新push时就会提示输入用户名和密码
git push origin 2.8_cn
Username for 'https://gitlab.hillstonenet.com': shunyu
Password for 'https://shunyu@gitlab.hillstonenet.com':

```

