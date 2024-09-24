if [ ! -d "logs" ]; then
  mkdir logs
fi

# 设置环境变量
export ENVIRONMENT='production'
echo  $ENVIRONMENT

pgrep -f "api.py" | xargs kill -9

if [ $? -eq 0 ];then
  echo "api.py process have been killed"
else
  echo "No api.py living"
fi

port=8000
#local_ip=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | grep -E '^20.' )
local_ip=0.0.0.0

echo $local_ip

nohup python3.9 -u api.py --host $local_ip --port $port >./logs/api.log 2>&1 &