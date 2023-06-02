### https://app2094.acapp.acwing.com.cn/

系统设置在: ./acapp/settings
功能实现在: ./game

game/models：数据库定义  
game/views：处理http的后端代码(登陆注册)  
game/consumers：处理websocket的后端代码(联机对战)  
game/urls：http路由  
game/routings.py：websocket路由  
match_system: thrift实现的rpc匹配系统  

game/static：静态文件，前端js代码都在这里。包含三个文件夹：js, css, image  
其中dist/zbase.js是所有src中的js代码压缩成的，src是逻辑上的代码。  

主html界面：game/templates/multiends/web.html，主要作用就是从game/static/js/dist/game.js中引入js对象  

