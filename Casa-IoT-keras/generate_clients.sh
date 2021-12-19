#!/bin/bash

casa_numbers=27   # min =1, max =27
client_numbers=10 #max= 10 , starts from 0
reducer_host='reducer'
combiner_name='combiner'
combiner_ip='Combiner-IP'

clients_counter=1
 echo "Generate docker-compose.yaml file"
 {
    printf "version: '3.3'\n"; shift
    printf 'services:\n'; shift

    for (( casa=1; casa<=$casa_numbers; casa++ ))
    do

      for (( client=0; client<=$client_numbers; client++ ))
      do
        printf "  client$clients_counter:\n"; shift
        printf '    environment:\n'; shift
        printf '      - GET_HOSTS_FROM=dns\n'; shift
        printf '    image: "casa:latest"\n'; shift
        printf '    build:\n'; shift
        printf '      context: .\n'; shift
        printf '    working_dir: /app\n'; shift
        printf '    command: /bin/bash -c "fedn run client -in client.yaml"\n'; shift
        printf '    volumes:\n'; shift
        printf "      - ./data/casa$casa/c$client:/app/data\n"; shift
        printf"       - ./client.yaml:/app/client.yaml"; shift
        ((++clients_counter))

      done

    done


}  >docker-compose.yaml



    echo "Generate client.yaml file"
    {
        printf "network_id: reducer-network\n"; shift
        printf "controller:\n"; shift
        printf "    discover_host: $reducer_host\n"; shift
        printf "    discover_port: 8090\n"; shift
        printf "    token: reducer_token \n \n"; shift
    } >client.yaml



    ### Generate extra-hosts-client.yaml file
    echo "Generate extra-hosts.yaml file"
    {
      printf "version: '3.3'\n"; shift
      printf 'services:\n'; shift

      for (( client=1; client<$clients_counter; client++ ))
       do

        printf "   client$client:\n"; shift
        printf '    extra_hosts:\n'; shift
        printf '      %s: %s \n' "$combiner_name" "$combiner_ip"

      done
    } > extra-hosts.yaml


        ### Generate private-network.yaml file
    echo "Generate private-network.yaml file"
    {
      printf "version: '3.3'\n"; shift
      printf 'networks:\n'; shift
      printf "   default:\n"; shift
      printf '    external:\n'; shift
      printf '      name: fedn_default \n'; shift

    } > private-network.yaml


