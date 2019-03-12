#!/bin/bash

set -e

host_name="$1"
shift
port="$1"
shift
overridden_command="$@"

until $(nc -z "$host_name" "$port"); do   
  >&2 echo "Neo4J is not available yet. Waiting for three second."
  sleep 3
done

>&2 echo "Neo4J is available now. Executing the default command."
eval $overridden_command
