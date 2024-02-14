#!/usr/bin/env bash

gq https://gql.api.alison.legislature.state.al.us/graphql -H "Content-type: application/json" -q '{committees(direction:"asc"orderBy:"committee"limit:"15"offset:"0" customFilters: {}){ CommitteeId,Committee,CommitteeClerk,CommitteeContact,CommitteePhone,ContactLocation }}' | jq '.data.committees' | jq -r '(.[0] | keys_unsorted) as $keys | $keys, map([.[ $keys[] ]])[] | @csv' > committees.csv
