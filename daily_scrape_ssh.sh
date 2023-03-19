Xvfb :99 -ac
DISPLAY=:99 java -jar selenium-server-standalone-2.4.0.jar

echo 'selenium server started'

. /opt/python/3.8a/bin/activate
conda activate sportBot

echo 'running scrape'
python3 slack_text_generator.py
