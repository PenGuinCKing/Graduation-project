# Graduation-project
毕业设计-火车票售票系统

## 项目结构

- `.idea/`: IntelliJ IDEA 项目配置文件夹。
- `App/`: Django 的核心应用文件夹，包含项目的模型（`models.py`）、视图（`views.py`）、URL配置（`urls.py`）等业务逻辑代码。
- `README.md`: 项目说明文件。
- `manage.py`: Django 项目的管理脚本，用于执行如启动服务器、数据库迁移等命令。
- `requirements.txt`: 列出了项目运行所需的所有 Python 依赖库及其版本。
- `static/`: 存放静态文件，包括：
    - `css/`: 层叠样式表文件，用于定义页面外观。
    - `img/`: 图片资源。
    - `js/`: JavaScript 文件，用于实现前端交互逻辑。
    - `live2d-widget/`: Live2D 看板娘的相关资源，用于在页面上显示动态的虚拟角色。
- `templates/`: 存放 HTML 模板文件，Django 通过这些模板渲染动态网页。
- `train_ticket/`: Django 项目的配置文件夹，包含：
    - `settings.py`: 项目的配置文件，如数据库设置、静态文件路径、中间件等。
    - `urls.py`: 项目的主 URL 配置文件，定义了 URL 到视图函数的映射关系。
    - `wsgi.py` 和 `asgi.py`: 分别用于 WSGI 和 ASGI 兼容的 Web 服务器的入口点。
- `uwsgi.ini`: uWSGI 服务器的配置文件，通常用于生产环境部署。
- `uwsgi/`: 存放 uWSGI 相关的日志和进程 ID 文件。

## 项目运行原理

本项目是一个典型的 Django Web 应用，其运行流程如下：

1.  **环境准备**：
    *   确保已安装 Python 环境。
    *   通过 `pip install -r requirements.txt` 命令安装 `requirements.txt` 文件中列出的所有依赖库。关键依赖包括 `Django` (Web框架), `djangorestframework` (用于构建API), `PyMySQL` (MySQL数据库驱动), `requests` (HTTP请求库), `beautifulsoup4` 和 `lxml` (可能用于数据抓取或解析) 等。

2.  **数据库配置与迁移**：
    *   在 `train_ticket/settings.py` 文件中，配置 `DATABASES` 项，指定数据库类型（根据 `PyMySQL` 推断为 MySQL）、名称、用户名、密码、主机和端口。
    *   执行数据库迁移命令：
        ```bash
        python manage.py makemigrations
        python manage.py migrate
        ```
        这些命令会根据 `App/models.py` 中定义的模型在数据库中创建相应的表结构。

3.  **启动开发服务器**：
    *   在项目根目录下，执行命令：
        ```bash
        python manage.py runserver
        ```
    *   Django 开发服务器会启动，默认监听 `http://127.0.0.1:8000/`。
    *   用户通过浏览器访问该地址即可与应用交互。

4.  **请求处理流程**：
    *   用户在浏览器中操作，发起 HTTP 请求（如访问页面、提交表单等）。
    *   请求到达 Django 后，首先由 `train_ticket/urls.py` 和 `App/urls.py` 中定义的 URL 路由规则进行匹配。
    *   匹配成功后，请求被分发到 `App/views.py` 中对应的视图函数进行处理。
    *   视图函数执行业务逻辑，这可能包括：
        *   从数据库中读取数据或向数据库写入数据（通过 `App/models.py` 中定义的 ORM 模型）。
        *   处理用户输入数据。
        *   调用其他服务或库。
    *   视图函数处理完毕后，会选择一个 HTML 模板（位于 `templates/` 目录下），并将处理结果数据传递给模板进行渲染。
    *   模板引擎将数据嵌入到 HTML 结构中，生成最终的 HTML 页面。
    *   生成的 HTML 页面作为 HTTP 响应返回给用户的浏览器进行显示。

5.  **前端交互**：
    *   浏览器加载 HTML 页面后，会执行页面中引用的 JavaScript 文件（位于 `static/js/`），这些脚本负责处理前端的动态效果和用户交互，例如表单验证、AJAX 请求等。
    *   页面的样式由 CSS 文件（位于 `static/css/`）控制。
    *   `static/live2d-widget/` 目录下的资源用于实现页面右下角的 Live2D 看板娘，为用户提供更丰富的交互体验。

6.  **核心功能模块（推断）**：
    *   **用户系统**：包括用户注册、登录、个人信息管理、密码修改等功能。
    *   **票务系统**：包括车次查询、车票预订、订单管理、在线支付（可能通过第三方接口）等。
    *   **后台管理系统**：供管理员使用，包括用户信息管理、车次管理、票务信息管理、站点管理、订单管理等。

7.  **生产环境部署（可选）**：
    *   对于生产环境，通常不会直接使用 `python manage.py runserver`。
    *   项目配置了 `uwsgi.ini`，表明可以使用 uWSGI 作为应用服务器，并通常会配合 Nginx 作为反向代理和静态文件服务器进行部署，以获得更好的性能和稳定性。
