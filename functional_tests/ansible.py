# Ansible提供了一个在线playbook分享平台，地址：https://galaxy.ansible.com/，
# 该平台汇聚了各类常用功能的角色（Role），当前分为web、system、packaging、
# networking、monitoring、development、database：sql、database：nosql、
# database、clustering、cloud：rax、cloud：gce、cloud：ec2、cloud共14类，
# 已经超过4000个功能角色。

# 根据需要找到适合你的角色后，只需要使用命令“ansible-galaxy install+作者ID. 角色包
# 名称”就可以安装到本地，比如想安装debops提供的Nginx安装与配置的角色，直接运行
# “ansible-galaxy install debops.nginx”即可安装到本地，该角色的详细地址为：
# https://galaxy.ansible.com/list#/roles/1580。

# 可以用user模块对用户授权，确保系统有一个deploy用户，并且属于web组，代码如下：
# user: name=deploy group=web


# 从源码安装过程如下：
# 1）提取Absible源代码：
# $ git clone git://github.com/ansible/ansible.git --recursive
# $ cd ./ansible
# $ source ./hacking/env-setup

# 如果想要安装过程中减少告警/错误信息输出，可以在安装时加上-q参数：
# $ source ./hacking/env-setup -q

# 2）如果系统没有安装过pip，先安装对应Python版本的pip:
# $ sudo easy_install pip

# 3）安装Ansible控制主机需要的Python模块：
# $ sudo pip install paramiko PyYAML Jinja2 httplib2 six

# 4）当更新Ansible版本时，不但要更新git的源码树，还要更新git中指向Ansible自身的模块，
# 称为submodules：
# $ git pull --rebase
# $ git submodule update --init --recursive

# 5）一旦运行env-setup脚本，就意味着Ansible从源码中运行起来了。
# 默认的资源清单inventory文件是/etc/ansible/hosts，清单文件inventory可以指定其他
# 位置：
# .. code-block:: bash
# $ echo "127.0.0.1" > ～/ansible_hosts
# $ export ANSIBLE_HOSTS=～/ansible_hosts


# 2. Tar包安装方式
# 不想通过GitHub提取方式获得Ansible的软件包，可以直接下载Ansible的Tar包，
# 下载地址是http://releases.ansible.com/ansible。
# Tar包的安装过程与上述源码安装方式一样，只是源代码获取方式不同而已。


# 3. 制作rpm包安装方式
# 有时需要制作成rpm软件包再进行安装。在GitHub上An-sible项目中提取软件，或直接下载
# 一个Tar包，然后使用makerpm命令创建RPM软件包，最后可分发这个软件包，或者使用它来
# 安装Ansible。在创建之前，先确定已安装了rpm-build、make、python2-devel组件。
# 操作过程如下(centos)：
# $ git clone git://github.com/ansible/ansible.git
# $ cd ./ansible
# $ make rpm
# $ sudo rpm -Uvh ～/rpmbuild/ansible-*.noarch.rpm
# 在Debian/Ubuntu环境中，可以采用类似的方法制作安装包，制作的命令是$make deb。


# 1. yum安装方式
# 要使用yum方式安装，需要有合适的yum源。Fedora用户只要连接着因特网，就可以直接使用
# 官方的yum源安装。但对于RHEL、CentOS的官方yum源中没有Ansible安装包，这就需要先安
# 装支持第三方的yum仓库组件，最常用的有EPEL、Remi、RPMForge等。在国内速度较快的高
# 质量yum源有
# 中国科技大学（http://mirrors.ustc.edu.cn）、
# 浙江大学（http://mir-rors.zju.edu.cn/epel/）、
# 上海交通大学（http://ftp.sjtu.edu.cn/fedora/epel/）、
# 网易163（http://mirrors.163.com）、
# sohu镜像源（http://mirrors.sohu.com/fedora-epel/）等。
# 下面安装EPEL作为部署Ansible的默认yum源。

# RHEL（CentOS）6版本：
# rpm  –Uvh http:// mirrors.zju.edu.cn/epel/6/x86_64/epel-release-6-8.noarch.rpm
# rpm  –Uvh http:// mirrors.zju.edu.cn/epel/6/i386/epel-release-6-8.noarch.rpm
# RHEL（CentOS）7版本：
# rpm  –Uvh http://
# mirrors.zju.edu.cn/epel/7/x86_64/e/epel-release-7-5.noarch.rpm

# 准备好yum源之后，Ansible就可直接用yum命令安装了，命令如下：
# $ sudo yum install ansible


# 2. Apt（Ubuntu）安装方式
# Ubuntu编译版可在如下地址中获得：https://launch-pad.net/～ansible/+archive/ansible。
# 通过执行如下命令直接安装：
# $ sudo apt-get install software-properties-common
# $ sudo apt-add-repository ppa:ansible/ansible
# $ sudo apt-get update
# $ sudo apt-get install ansible


# 3. Homebrew（Mac OSX）安装方式
# 在Mac系统中，确定已经安装了Homebrew之后，直接执行下面命令安装Ansible：
# $ brew update
# $ brew install Ansible

# 4. pip方式安装Ansible也支持可通过pip方式安装。pip是Python软件包的安装和管理工具，
# 执行如下命令先安装pip：
# $ sudo easy_install pip

# 然后再安装Ansible：
# $ sudo pip install ansible

# 如果你是在OS X系统上安装，编译器可能会有警告或出错，需要设置CFLAGS、CPPFLAGS环境变量：
# $ sudo CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install ansible

# 使用virtualenv的读者可通过virtualenv安装Ansible，然而不建议这样做，直接在全局
# 安装Ansible。不要使用easy_install直接安装Ansible。如果把Ansible安装在其他相对少
# 见的Linux操作系统（如Gentoo、FreeBSD等）上，详见Ansible官网
# http://docs.ansi-ble.com。


# 配置运行环境
# 配置Ansible环境
# Ansible配置文件是以ini格式存储配置数据的，在Ansible中，几乎所有的配置项都可以通过
# Ansible的playbook或环境变量来重新赋值。在运行Ansible命令时，命令将会按照预先设定的
# 顺序查找配置文件，如下所示：
# 1）ANSIBLE_CONFIG：
# 首先，Ansible命令会检查环境变量，及这个环境变量将指向的配置文件。
# 2）./ansible.cfg：其次，将会检查当前目录下的ansible.cfg配置文件。
# 3）～/.ansible.cfg：再次，将会检查当前用户home目录下的.ansible.cfg配置文件。
# 4）/etc/ansible/ansible.cfg：最后，将会检查在用软件包管理工具安装Ansible时自动
# 产生的配置文件。
# 注意　如果你通过操作系统软件包管理工具或pip安装，那么你在/etc/ansible目录下应该
# 已经有了ansible.cfg配置文件；如果你是通过GitHub仓库安装的，
# 在你复制的仓库中examples目录下可以找到ansible.cfg，你可以把它拷贝到
# /etc/ansible目录下。


# 执行：ssh-key-gen-t rsa，有询问直接按回车键即可，将在/root/.ssh/下生成一对密钥，
# 其中id_rsa为私钥，id_rsa.pub为公钥

# 下发密钥就是控制主机把公钥id_rsa.pub下发到被管节点上用户下的.ssh目录，并重命名
# 成authorized_keys，且权限值为400。接下来推荐常用的密钥拷贝工具ssh-copy-id，
# 把公钥文件id_rsa.pub公钥拷贝到被管节点
# ssh-copy-id -i /root/.ssh/id_rsa.pub root@192.168.1.111

# 密钥分发后，需要验证一下SSH无密码配置是否成功，只需运行ssh root@192.168.1.111，
# 如果直接进入被管节点root账号提示符，即出现[root@web1～]#，则说明配置成功。
# 同样的配置方式对web2（192.168.1.112）也做下密钥分发。


# 测试连通性，首先下发密钥, 然后/etc/ansible/hosts
# [webservers]
# #web1.ansible.cn
# #web2.ansible.cn
# 116.85.48.20
# 116.85.59.2

# host_key_checking = False
# remote_user = dc2-user

# $ ansible webservers -m ping


# 在webservers组服务器上显示hello ansible
# $ ansible webservers -m shell -a '/bin/echo hello ansible!'
# 也可以使用command模块
# $ ansible webservers -m command -a '/bin/echo hello ansible!'


# ansible-doc工具的支持参数。最主要的参数-l列出可使用的模块，-s列出某个模块支持的动作
# 如下面列出yum模块的动作：
# $ ansible-doc -s yum


# 另外，在Ansible调试自动化脚本时候经常需要获取执行过程的详细信息，可以在命令后面添加
# -v或-vvv得到详细的输出结果。如：
# $ ansible webservers -i inventory.cfg -m ping –vvv


# Ansible Inventory
# 在大规模的配置管理工作中我们需要管理不同业务的不同机器，这些机器的信息都存放在
# Ansible的Inventory组件里面。在我们工作中配置部署针对的主机必须先存放在Inventory
# 里面，这样才能使用Ansible对它进行操作。默认Ansible的In-ventory是一个静态的INI格式
# 的文件/etc/ansible/hosts，当然，还可以通过ANSIBLE_HOSTS环境变量指定或者运行
# ansible和ansible-playbook的时候用-i参数临时设置。1. 定义主机和主机组下面我们来看一
# 下如何在默认的Inventory文件中定义一些主机和主机组，具体如下：
# 1 172.17.42.101   ansible_ssh_pass='123456'
# 2 172.17.42.102   ansible_ssh_pass='123456'
# 3 [docker]
# 4 172.17.42.10[1:3]
# 5 [docker:vars]
# 6 ansible_ssh_pass='123456'
# 7 [ansible:children]
# 8 docker
# •第1行定义了一个主机是172.17.42.101，然后使用Inventory内置变量定义了SSH登录密码。
# •第2行定义了一个主机是172.17.42.102，然后使用Inven-tory内置变量定义了SSH登录密码。
# •第3行定义了一个组叫docker。
# •第4行定义了docker组下面4台主机从172.17.42.101到172.17.42.103。
# •第5行到第6行针对docker组使用Inventory内置变量定义了SSH登录密码。
# •第7行到第8行定义了一个组叫ansible，这个组下面包含docker组。

# $ ansible 172.17.42.101:172.17.42.102 -m ping -o
# $ ansible docker -m ping -o
# $ ansible ansible -m ping -o


# # 多个inventory文件
# [root@Master ～]# tree inventory/
# inventory/
# ├── docker
# └── hosts

# 不同的文件可以存放不同的主机，我们来分别看一下文件的内容：
# [root@Master ～]# cat inventory/hosts
# 172.17.42.101   ansible_ssh_pass='123456'
# 172.17.42.102   ansible_ssh_pass='123456'
# [root@Master ～]# cat inventory/docker
# [docker]
# 172.17.42.10[1:3]
# [docker:vars]
# ansible_ssh_pass='123456'
# [ansible:children]
# docker
# 最后我们修改了ansible.cfg文件中inventory的值，这里不再指向一个文件，而是指向一个目录，
# 修改如下：
# inventory  = /root/inventory/

# 这样我们就可以使用Ansible的list-hosts参数来进行如下验证：
# [root@Master ～]# ansible 172.17.42.101:172.17.42.102 --list-hosts
# 172.17.42.101    172.17.42.102
# [root@Master ～]# ansible docker --list-hosts
# 172.17.42.101
# 172.17.42.102
# 172.17.42.103
# [root@Master ～]# ansible ansible --list-hosts
# 172.17.42.101
# 172.17.42.102
# 172.17.42.103
# 其实Ansible中的多个Inventory跟单个文件没什么区别，我们也可以容易定义或者引用多个
# Inventory，甚至可以把不同环境的主机或者不同业务的主机放在不同的Inventory文件里面，
# 方便日后维护。
