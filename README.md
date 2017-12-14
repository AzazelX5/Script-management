# Script-management
## 脚本管理
> 作用：将本地脚本同步到远程服务器中，方便在多台电脑上使用
> 
> 说明：
> > 1.目录结构
> > > src/ : 脚本管理服务器端代码
> > > Dockerfile: docker镜像制作
> > > script.py : 本地管理脚本与服务器同步的脚本
> > 
> > 2.使用方法
> > > (1) 服务器端：将src/和Dockerfile拷贝到远程服务器，用Dockerfile制作镜像后开启即可；也可以到src/目录下运行Djnago服务器
> > > 
> > > (2) 本地：将script.py拷贝到本地管理脚本的文件夹下，打开shell,通过以下命令管理脚本
> > > > **python script.py pull**：将服务器中的脚本下载到script.py所在的文件夹
> > > > 
> > > > **python script.py push**：将script.py所在的文件夹下的脚本上传到服务器
> > > > 
> > > > **python script.py ls[-a]**：查看服务器中的脚本列表，脚本ID默认显示8位，加-a参数可以显示全部ID
> > > > 
> > > > **python script.py search[-a] (脚本ID)**：模糊查询服务器中的脚本(-a作用同上)
> > > > > 注：脚本ID采用UUID，模糊查询是按照ID从头到尾开始匹配，比如search 5 表示查询脚本ID以5开头的所有脚本，search 5a表示查询脚本ID以5a开头的所有脚本，以此类推
> > > > 
> > > > **python script.py del (参数)**：删除脚本功能 **（暂未实现，努力实现中。。。）**
> >
> > 3.其它
> > > 数据库：由于数据量不大，所以采用sqlite数据库，存放在src/文件夹下

