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


## 前端逻辑
settings：登陆注册界面  
menu：登陆成功后的界面  
playground：游戏界面 

### 1.menu：
menu/zbase.js：登陆成功后的菜单，三个button分别是单人模式，多人模式，退出(退出至登陆界面)。button会调用playground.show() 

### 2.playground:
playground/zbase.js：Playground类，是游戏界面的主类，主要有两个关键的方法show(), hide()负责打开和隐藏playground界面。show(mode)根据不同的模式（单人/多人）选择创建ws连接还是直接加入ai。 

playground/ac_game_object/zbase.js：定义了一个AcGameObject的基类，有uuid，当到一个全局的AC_GAME_OBJECTS数组中。仿照unity有start(), update(), late_update(), destroy()等基本方法，是游戏中所有对象的基类。还定义了一个AC_GAME_ANIMATION函数，用于控制游戏的帧动画。通过递归调用js的requestAnimationFrame()方法实现的。 

playground/game_map/zbase.js：定义了游戏地图，继承自AcGameObject，创建一个js的canvas对象，获取其2D绘图上下文；另加了resize()用于浏览器窗口更改时的适配和render()用于地图渲染. 

playground/player/zbase.js：定义了玩家对象，继承自AcGameObject。属性有：
1. playground: 游戏场景对象
1. x和y: 玩家的位置坐标
1. vx和vy: 玩家的速度分量
1. damage_x和damage_y: 玩家受伤后的位移分量
1. damage_speed: 玩家受伤后的速度
1. move_length: 玩家当前移动的距离
1. ctx: 画布的上下文对象
1. radius: 玩家的半径
1. color: 玩家的颜色
1. speed: 玩家的移动速度
1. character: 玩家的角色类型
1. username: 玩家的用户名
1. photo: 玩家的照片
1. friction: 玩家受伤后的摩擦系数
1. spent_time: 玩家已经花费的时间，未到事件不允许攻击
1. eps: 很小的数值，用于比较0
1. fireballs: 玩家发射的火球数组
1. img: 玩家的图像对象（非机器人角色）
1. fireball_coldtime: 玩家发射火球的冷却时间
1. fireball_image: 火球的图像对象
1. blink_coldtime: 玩家闪烁技能的冷却时间
1. blink_image: 闪烁技能的图像对象
1. cur_skill: 当前选择的技能


方法:   
constructor(): 构造函数，用于初始化玩家对象的属性  
start(): 游戏开始时调用的方法，增加玩家计数并判断是否开始战斗 
add_listening_events(): 添加监听事件，包括鼠标点击、键盘按键等操作  
shoot_fireball(tx, ty): 发射火球的方法，返回发射的火球对象  
destroy_fireball(uuid): 销毁指定uuid的火球  
blink(tx, ty): 玩家闪现的方法  
is_attacked(angle, damage): 玩家受到攻击时的处理方法  
receive_attack(x, y, angle, damage, ball_uuid, attacker): 接收来自其他玩家的攻击  
get_dist(x1, y1, x2, y2): 计算两点之间的距离  
move_to(tx, ty): 移动到指定位置的方法  
update(): 更新玩家状态和画面的方法  
update_win(): 更新胜利状态的方法  
update_coldtime(): 更新技能冷却时间的方法  
update_move(): 更新玩家移动状态的方法  
render(): 渲染玩家和技能冷却时间的方法  
render_skill_coldtime()：渲染图标冷却的方法  
on_destroy()：玩家被击败。  



playground/skill/fireball/zbase.js：有一些基本的火球参数；该类的主要功能就是在update中检测其是否与其他players有碰撞，如果有就调用对方的is_attacked()方法并销毁自己即可 

playground/particle/zbase.js：火球技能击中敌人时的特效粒子。发生碰撞时会随机向不同方向生成随机多的粒子，速度较快，分散距离小，会较快消失。 

playground/notice_board/zbase.js：游戏界面上方的显示板，多人模式下显示其就绪人数，人满了就显示"fighting!" 

playground/chat_field/zbase.js：聊天区。不再是AcGameObject的子类了。监听键盘事件，enter会获取输入框中的信息并输入，esc会隐藏聊天区域。发信息或收到信息会显示历史记录一段时间，之后自动隐藏。 

playground/score_baord/zbase.js：得分板，在player.update_win()检测到players只剩一个或player.destroy()时调用其win/lose方法，会展示相应的图像，然后在点击屏幕回到主菜单。 

playground/socket/multiplayer/zbase.js: 
    http是一种请求-响应的通信协议，只有客户端请求才有服务端的响应，这对于需要多端同步的联机游戏显然是不可取的，http可以通过长轮询的方式实现类似服务器主动发送信息的形式，但是效率不高且负载高，所以程序引入了双向通信和持久连接的websocket协议。 
    连接到指定的wss服务器，receive监听wss服务器的消息，以uuid为通信基准。get_player找到指定的对象，send_, receive_函数进行与服务器的通信。 

### 3.settings:
settings/zbase.js：这是登录注册的界面，主要是通过ajax用http协议与服务器异步通信。 
