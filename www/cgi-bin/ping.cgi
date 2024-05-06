#!/bin/bash

ip_address=""
declare -a ports

IFS='&' read -ra PARAMS <<< "$QUERY_STRING"

found_ip=false

for PARAM in "${PARAMS[@]}"; do
    IFS='=' read -ra PAIR <<< "$PARAM"
    if [ "${PAIR[0]}" == "ip_address" ]; then
        ip_address="${PAIR[1]}"
        if [ -z "$ip_address" ]; then
            found_ip=false
        else
            found_ip=true
        fi
    fi
done


echo "Content-type: text/html; charset=utf-8"
echo ""
# echo "<html>"
# echo "<body>"
echo "<h1>Kiểm tra</h1>"

echo "<p>"
if [ "$found_ip" == true ]; then
    echo "Địa chỉ IP: $ip_address </p>"
    echo "<p>Kiểm tra Ping</p>"
    echo "<p>"
    ping "$ip_address" -c 4 |head -n -3 | while read line; do
        echo "$line <br>"
    done
    echo "<p>Kiểm tra các cổng</p>"
    sudo nmap "$ip_address" | tail -n +5 | head -n -2 |while read line;do
        echo "$line <br>"
    done
    sudo nmap -sU -p 53,67,68,161,137-138,69,123 "$ip_address" | tail -n +5 | head -n -2 |while read line;do
        echo "$line <br>"
    done
else
    echo "Không tìm thấy IP address trong yêu cầu."
fi

echo "</p>"
# echo "</body>"
# echo "</html>"

