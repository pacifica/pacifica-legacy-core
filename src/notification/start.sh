#!/bin/bash

./emsl-notify --script ./expresso.sh --xpath '/myemsl[instrument="SOLID1"]' --statedb ./expresso.db
./emsl-notify --script ./hadoop.sh --xpath '/myemsl[instrument="Expresso-Bioscope"]' --statedb ./hadoop.db
./emsl-notify --script ./nwchem.sh --xpath '/myemsl[instrument="4NWChem"]' --statedb ./nwchem.db
./emsl-notify --script ./email.sh --xpath '/myemsl[proposal="1273981"]' --statedb ./email.db
