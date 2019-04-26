# exit on error
set -e

# run Pilosa on the background, so we can import into it
/pilosa server -b :10101 -d /data &
PILOSA_PID=$!

# wait a bit for Pilosa to finish initializing
sleep 5

# create the schema and import
/pilosa import --host :10101 -e -i repository -f language /getting-started/language.csv
/pilosa import --host :10101 -e -i repository -f stargazer --field-type time --field-time-quantum YMD /getting-started/stargazer.csv

# stop Pilosa
kill -INT $PILOSA_PID
wait $PILOSA_PID
