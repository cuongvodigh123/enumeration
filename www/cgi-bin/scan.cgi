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
    elif [ "${PAIR[0]}" == "port" ]; then
        IFS=',' read -ra PORTS <<< "$(echo "${PAIR[1]}" | sed 's/%2C%20/,/g')"
        for port in "${PORTS[@]}"; do 
	    ports+=("$port")       
	done
    fi
done

echo "Content-type: text/html; charset=utf-8"
echo ""
# echo "<html>"
# echo "<body>"
echo "<p>"
if [ "$found_ip" == true ]; then
    echo "Địa chỉ IP: $ip_address </p>"
    echo "<p>Các cổng được chọn: "
    for port in "${ports[@]}"; do
        echo "$port "
    done
	echo "</p>"

    if [[ " ${ports[@]} " =~ " 21 " ]]; then
        echo "<h1>Thu thập FTP</h1>"
        echo "<p>"
        sudo nmap -sC -p 21 $ip_address | tail -n +3 | head -n -2| while read line;do
            echo "$line <br>"
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 22 " ]]; then
        echo "<h1>Kiểm tra dịch vụ SSH</h1>"
        echo "<p>"
        sudo nmap -p 23 $ip_address | tail -n +4 | head -n -2| while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 23 " ]]; then
        echo "<h1>Kiểm tra dịch vụ telnet</h1>"
        echo "<p>"
        sudo nmap -p 22 $ip_address | tail -n +4 | head -n -2| while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 25 " ]]; then
        echo "<h1>Thu thập SMTP</h1>"
        echo "<p>"
        sudo nmap -p 25 --script=smtp-enum-users,smtp-commands,smtp-open-relay $ip_address | tail -n +4 | head -n -3| while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 53 " ]]; then
        echo "<h1>Thu thập DNS</h1>"
        result=$(nslookup -p $ip_address)
        echo "<p>$result</p>"
        name_value=$(echo "$result" | awk '/name/ {print $NF}')
        domain=$(echo "$name_value" | cut -d'.' -f2-)
        echo "<p>Domain: $domain</p>"
        echo "<p>Thu thập các bản ghi DNS từ domain có được<br>"
        sudo dnsrecon -d $domain | while read line;do
            echo "$line <br>"
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 69 " ]]; then
        echo "<h1>Thu thập TFTP</h1>"
        echo "<p>"
        sudo nmap -p 69 $ip_address | tail -n +3 | head -n -2| while read line;do
            echo "$line <br>"
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 80 " ]]; then
        echo "<h1>Thu thập HTTP</h1>"
        echo "<p>"
        sudo nmap -sC -p 80 $ip_address | tail -n +3 | head -n -2| while read line;do
            echo "$line <br>"
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 111 " ]]; then
        echo "<h1>Thu thập RPCinfo</h1>"
        result=$(sudo rpcinfo -p $ip_address)
        echo "<p>$result</p>"
        if echo "$result" | grep -q nfs; then
            echo "<p>Dịch vụ NFS đã được tìm thấy.</p>"
            echo "<p>"
            sudo showmount -e $ip_address | while read line;do
                echo "$line <br>"
            done
            echo "</p>"
        fi
    fi

    if [[ " ${ports[@]} " =~ " 123 " ]]; then
        echo "<h1>Thu thập NTP<h1>"
        echo "<p>"
        sudo ntpdate -d $ip_address | while read line;do
            echo "$line <br>" 
        done
        sudo ntptrace -n $ip_address | while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 139 " ]]; then
        echo "<h1>Thu thập NetBIOS</h1>"
        echo "<p>"
        sudo nbtscan -v $ip_address | while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi


    if [[ " ${ports[@]} " =~ " 161 " ]]; then
        echo "<h1>Thu thập SNMP</h1>"
        echo "<p>"
        sudo snmp-check $ip_address | awk '$1 != "0.0.0.0"'| while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 179 " ]]; then
        echo "<h1>Thu thập BGP</h1>"
        echo "<p>"
        sudo nmap -p 179 $ip_address | while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 389 " ]]; then
        echo "<h1>Kiểm tra xem ldap</h1>"
        sudo ldapsearch -x -H ldap://$ip_address | while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 445 " ]]; then
        echo "<h1>Thu thập SMB</h1>"
        echo "<p>"
        sudo nmap -p 445 -A $ip_address | tail -n +4 | head -n -2| while read line;do
            echo "$line <br>"
        done
        sudo nmap -p 445 --script smb-protocols $ip_address | tail -n +4 | head -n -1| while read line;do
            echo "$line <br>"
        done
        echo "</p>"
    fi

    if [[ " ${ports[@]} " =~ " 500 " ]]; then
        echo "<h1>Kiểm tra dịch vụ VPN</h1>"
        echo "<p>"
        sudo ike-scan -M $ip_address| while read line;do
            echo "$line <br>" 
        done
        echo "</p>"
    fi

    

fi
else
    echo "Không tìm thấy IP address trong yêu cầu."
fi
echo "</p>"
# echo "</body>"
# echo "</html>"

