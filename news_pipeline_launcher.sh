#!/bin/zsh
# redis-server &
# mongod &

# pip install -r requirements.txt

cd news_pipeline
python news_monitor.py &
python news_fetcher.py &
python news_deduper.py &

cd ../news_topic_modeling_service/server
python server.py &

echo "============================"
read -p "PRESS [ANY KEY] TO TERMINATE PROCESSES." PRESSKEY

kill $(jobs -p)
