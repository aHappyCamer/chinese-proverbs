#!/bin/bash

if curl -s --head  --request GET https://chineseproverbs.duckdns.org | grep "200 OK" > /dev/null; then     
    echo "website is UP"; 
else    
    echo "website is DOWN"; 
fi