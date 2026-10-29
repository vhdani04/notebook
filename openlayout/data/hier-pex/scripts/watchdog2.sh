# kill any of my PEX / FasterCap processes above 7.5 GB RSS; log memory every minute
while true; do
  ps -eo pid=,rss=,args= | awk '/[o]penlayout\.pex|[F]asterCap/ && $2 > 7500000 {print $1}' | xargs -r kill
  used=$(free -m | awk '/Mem:/ {print "used " $3 " MB, available " $7 " MB"}')
  pex=$(ps -eo rss=,comm= | awk '/python3|FasterCap/ {s += $1} END {print int(s / 1024)}')
  echo "$(date +%T) $used, pex rss $pex MB" >> /tmp/xs/watchdog.log
  sleep 60
done
