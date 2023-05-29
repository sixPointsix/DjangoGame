#! /bin/bash

# 将src中的所有js文件打包成一个放到dist中

JS_PATH=/home/xzy/acapp/game/static/js/
JS_PATH_DIST=${JS_PATH}dist/
JS_PATH_SRC=${JS_PATH}src/

find ${JS_PATH_SRC} -type f -name '*.js' | sort | xargs cat > ${JS_PATH_DIST}game.js

echo yes | python3 manage.py collectstatic
