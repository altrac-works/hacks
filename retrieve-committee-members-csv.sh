#!/usr/bin/env bash

TAIL="+1" #tail does nothing
echo -n > committee-members.csv #clear the file

for ID in $(cat committees.csv | tail -n +2 | cut -d ',' -f 1 | jq -r); do
    >&2 echo "id $ID"
    gq https://gql.api.alison.legislature.state.al.us/graphql -H "Content-type: application/json" -q '{membersByCommittee( committeeId:"'$ID'" ) { Committee MemberName MemberPosition }}' | jq '.data.membersByCommittee' | jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' | tail -n "$TAIL" >> committee-members.csv

    TAIL="+2" #for every run after the first, tail will not output the first line (headers)
done
