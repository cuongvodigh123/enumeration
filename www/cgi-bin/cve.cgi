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

echo "<p>"
if [ "$found_ip" == true ]; then
    echo "Địa chỉ IP: $ip_address </p>"
    echo "<p>Kiểm tra CVE</p>"
    echo "<p>"
    sudo nmap --script=vulscan/vulscan.nse --script-args vulscandb=cve.csv -sV $ip_address | grep "CVE" | while read line;do
        echo "$line <br>"
    done
else
    echo "Không tìm thấy IP address trong yêu cầu."
fi

echo "</p>"
# echo "</body>"
# echo "</html>"

